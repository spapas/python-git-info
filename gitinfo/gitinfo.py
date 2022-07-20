import glob
import os
import zlib
import struct
import zlib


from .pack_reader import get_pack_info
from .helpers import parse_git_message


def find_git_dir(directory):
    "Find the correct git dir; move upwards if .git folder is not found here"
    absdir = os.path.abspath(directory)
    gitdir = os.path.join(absdir, ".git")
    if os.path.isdir(gitdir):
        return gitdir
    parentdir = os.path.dirname(absdir)
    if absdir == parentdir:
        # We reached root and found no gitdir
        return None
    return find_git_dir(parentdir)



def get_head_commit(directory):
    "Retrieve the HEAD commit of this repo had"
    head_file = os.path.join(directory, "HEAD")
    refs = None
    
    if not os.path.isfile(head_file):
        return
    
    head_parts = None
    
    if not os.path.isfile(head_file):
        return
    
    with open(head_file, "r") as fh:
        data = fh.read().strip()
        refs = data
        try:
            head_parts = data.split(" ")[1].split("/")
        except IndexError:
            # The head may contain just a commit so let's return it in that case:
            return data
    if not head_parts:
        return

    head_ref_file = os.path.join(directory, *head_parts)
    if not os.path.isfile(head_ref_file):
        return
    head_commit = None
    with open(head_ref_file, "r") as fl:
        head_commit = fl.read().strip()
        return head_commit, refs


def get_git_info_dir(directory):
    head_commit, refs = get_head_commit(directory)
    
    if not head_commit:
        return

    head_message_folder = head_commit[:2]
    head_message_filename = head_commit[2:]
    head_message_file = os.path.join(
        directory, "objects", head_message_folder, head_message_filename
    )

    if refs.startswith("ref: refs/heads/"):
        refs = refs[len("ref: refs/heads/"):]
    
    gi = {"commit": head_commit, "gitdir": directory, "message": "", "refs": refs}

    if not os.path.isfile(head_message_file):
        # Here we open the snake bucket of idx+pack
        object_path = os.path.join(directory, "objects", "pack")
        for idx_file in glob.glob(object_path + "/*.idx"):
            r = get_pack_info(idx_file, gi)
            if not r:
                continue
            return r

    else:
        with open(head_message_file, "rb") as fl:
            data = zlib.decompress(fl.read())
            if not data[:6] == b"commit":
                # Not a commit object for some reason...
                return
            # Retrieve the null_byte_idx and start from there
            null_byte_idx = data.index(b"\x00") + 1
            data = data[null_byte_idx:]
            
            return parse_git_message(data, gi)

        


def get_git_info(dir=os.getcwd()):
    gitdir = find_git_dir(dir)
    if not gitdir:
        return None
    return get_git_info_dir(gitdir)


if __name__ == "__main__":
    print(get_git_info())
