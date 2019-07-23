import struct
import binascii
import zlib
import os

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

