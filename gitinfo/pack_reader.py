import struct
import binascii
import zlib
import codecs
import os
from .helpers import parse_git_message

# Very useful info for pack and index files: https://codewords.recurse.com/issues/three/unpacking-git-packfiles

# Taken from here https://stackoverflow.com/a/312464/119071
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def convert_commit_to_bytes(commit):
    c = map(lambda z: int(z, 16), chunks(commit, 2))
    # Works with both py 2 and 3
    bc = bytes(bytearray(c))
    return bc 


def get_pack_idx(idx_file, commit):
    head_commit_bytes = convert_commit_to_bytes(commit)
    pack_idx = -1 
    with  open(idx_file, "rb") as fin:
        # Check header
        if fin.read(4) != b'\xff\x74\x4f\x63':
            return

        # Read number of objects: 
        # 8 bytes header + 1023 bytes that contain the number of objects that start with <= fe
        # so we'll reach number of objects that start with <= ff (all objects)
        fin.seek(1028, 0)

        tot_obj = struct.unpack('!I', fin.read(4))[0]
        # print("Total objects is {0}".format(tot_obj))

        found = False
        idx = 0 
        # TODO: This can be improved using binary search instead of seq seach... 
        while(idx <= tot_obj):
            inp=(fin.read(20))
            if inp == head_commit_bytes:
                found = True
                break
            idx+=1
        
        if not found:
            return None, None

        # Ok here we've found the index of our commit in the file. Let's get
        # its index in the pack file: The index file is something like:
        # 1032 (header (8) + objects number (4*256)) bytes
        # total_objects * 20 bytes each
        # total_objects * 4 bytes crc
        # and finally the pack index starts
        pack_idx_idx = 1032 + tot_obj*20 + tot_obj*4 + 4*idx
        # So let's go directly to that position in the file and read the pack index 
        fin.seek(pack_idx_idx, 0)
        pack_idx = struct.unpack('!I', fin.read(4))[0]
        # print("PACK IDX IS {0}".format(pack_idx))
        return pack_idx, tot_obj

def read_len(fin, byte0):

    len_barr = bytearray()
    len_barr.append(byte0 & 0x0f)

    # read the rest of the bytes of the length
    while(True):
        byt = struct.unpack('B', fin.read(1))[0]
        
        if (byt & 0x80): # MSB is 1 we need to reread
            
            len_barr.append(byt & 0x7f)
        else:
            len_barr.append(byt & 0x7f)
            break

    return int(codecs.encode(bytes(reversed(len_barr)), 'hex'), 16)

def read_len_from_bytes(array):
    len_barr = bytearray()
    # read the rest of the bytes of the length
    c = 0 
    while(True):
        byt = array[c]
        c+=1
        if (byt & 0x80): # MSB is 1 we need to reread
            len_barr.append(byt & 0x7f)
        else:
            len_barr.append(byt)
            break
    return array[c:], int(codecs.encode(bytes(len_barr), 'hex'), 16)    

def decode_delta(fin, data, r, pack_idx, offset):
    d0 = data[0]
    a+=1
    if(d0 & 0x80):
        # Copy data from other object
        oo = get_object(fin, pack_idx - offset )
        data = data[1:]
        
        offset = data[0]
        size = data[1]
        
        r+=oo[offset:offset+size]

        data = data[2:]
    else:
        # Insert raw data
        l = d0&0x7f
        dti = data[1:1+l]
        r+=dti
        data = data[1+l:]
 
    return data, r

def get_object(fin, pack_idx):
    fin.seek(pack_idx, 0)

    # Read the 1st byte
    byte0 = struct.unpack('B', fin.read(1))[0]
    # Make sure this is a commit object or an ofs delta
    if not (byte0 & 0x70) >> 4 in [1, 6]:
        return 

    if (byte0 & 0x70) >> 4 == 1: # OBJ_COMMIT 
        obj_len = read_len(fin, byte0)
        data = zlib.decompress(fin.read(obj_len))
        return data
    elif (byte0 & 0x70) >> 4 == 6: # OBJ_OFS_DELTA 
        obj_len = read_len(fin, byte0)
        byte0 = struct.unpack('B', fin.read(1))[0]
        offset = read_len(fin, byte0)
        data = zlib.decompress(fin.read(obj_len))

        # Read lengths (won't be used for now)
        data, l1 = read_len_from_bytes(data)
        data, l2 = read_len_from_bytes(data)
        
        # Decode the delta into the delta_res variable
        delta_res = b''
        while(len(data)):
            data, r = decode_delta(fin, data, delta_res, pack_idx, offset)

        return delta_res
    else:
        raise NotImplementedError("Not implemented yet!")
        

def get_pack_info(idx_file, gi):
    # Retrieve idx of our commit info in the pack file
    
    pack_idx, index_tot_objects = get_pack_idx(idx_file, gi['commit'])
    if not pack_idx:
        return 

    # Pack file has the same name as the index file
    pack_file = idx_file[0:-3]+"pack"

    with open(pack_file, "rb") as fin:
        # Check header
        if fin.read(4) != b'PACK':
            return
        fin.read(4) # ignore version

        # Make sure that the number of objects is the same as in index
        pack_total_objects = struct.unpack('!I', fin.read(4))[0]
        if index_tot_objects != pack_total_objects:
            return
        data = get_object(fin, pack_idx)

        return parse_git_message(data, gi)
