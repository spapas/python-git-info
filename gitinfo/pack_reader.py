import struct
import binascii
import zlib
import os
from .helpers import parse_git_message

# Very useful info for pack and index files:  https://codewords.recurse.com/issues/three/unpacking-git-packfiles

# Take from here https://stackoverflow.com/a/312464/119071
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def convert_commit_to_bytes(commit):
    c = map(lambda z: int(z, 16), chunks(commit, 2))
    bc = bytes(c)
    return bc 


def get_pack_info(idx_file, gi):
    idx_file_name = (os.path.splitext(os.path.basename(idx_file))[0])
    head_commit_bytes = convert_commit_to_bytes(gi['commit'])
    pack_idx = -1 
    with  open(idx_file, "rb") as fin:
        fin.seek(1028, 0)

        tot_obj = struct.unpack('!I', fin.read(4))[0]
        print("Total objects is {0}".format(tot_obj))

        found = False
        idx = 0 
        # TODO: This can be improved using binary search instead of seq seach... 
        while(not found):
            inp=(fin.read(20))

            if inp == head_commit_bytes:
                found = True
                print("Found at idx {0}".format(idx))
                break

            idx+=1
            if idx > tot_obj:
                break

        
        if not found:
            return

        correct_idx = 1032 + tot_obj*20 + tot_obj*4 + 4*idx
        fin.seek(correct_idx, 0)
        pack_idx = struct.unpack('!I', fin.read(4))[0]
        print("PACK IDX IS ".format(pack_idx))

    pack_file = idx_file[0:-3]+"pack"
    print("PACK FILE IS  ".format(pack_file))
    with open(pack_file, "rb") as fin:
        fin.seek(pack_idx, 0)

        b0 = fin.read(1)
        i0 = int.from_bytes(b0, byteorder='little') 

        if not (i0 & 0x70) >> 4 == 1:
            print("ERR")
            a+=1

        l0 = i0 & 0x0f

        b1 = fin.read(1)
        i1 = int.from_bytes(b1, byteorder='little') 
        print (b0, l0, b1, i1)

        l = (l0 << 4) + i1

        data = zlib.decompress(fin.read(l))
        return parse_git_message(data, gi)


            
        


