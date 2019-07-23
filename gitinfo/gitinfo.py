import glob
import os
import time
import zlib
import struct
import zlib

from gitinfo.pack_reader import  get_pack_info


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


def parse_commiter_line(line):
    #print(line)
    #print("~")
    "Parse the commiter/author line which also contains a datetime"
    parts = line.split()
    # TODO: I'll ignore tz for now It is parts[:-1]
    unix_time = float(parts[-2])
    commiter = " ".join(parts[1:-2])
    commit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))
    return commiter, commit_time


def get_head_commit(directory):
    "Retrieve the HEAD commit of this repo had"
    head_file = os.path.join(directory, "HEAD")
    if not os.path.isfile(head_file):
        return
    head_parts = None
    if not os.path.isfile(head_file):
        return
    with open(head_file, "r") as fh:
        data = fh.read().strip()
        try:
            head_parts = data.split(" ")[1].split("/")
        except IndexError:
            return
    if not head_parts:
        return

    head_ref_file = os.path.join(directory, *head_parts)
    if not os.path.isfile(head_ref_file):
        return
    head_commit = None
    with open(head_ref_file, "r") as fl:
        head_commit = fl.read().strip()
        return head_commit


def parse_git_message(data, gi):
    lines = data.decode("utf-8").split("\n")
    reading_pgp = False
    reading_msg = False

    for l in lines:
        if l == "":
            reading_pgp = False
            reading_msg = True
            continue

        if reading_pgp == True:
            continue

        if reading_msg == True:
            gi["message"] += l

        if l.startswith("tree"):
            gi["tree"] = l.split()[1]
        elif l.startswith("parent"):
            gi["parent"] = l.split()[1]
        elif l.startswith("gpgsig"):
            reading_pgp = True
        elif l.startswith("commiter"):
            commiter, commit_time = parse_commiter_line(l)
            gi["commiter"] = commiter
            gi["commit_date"] = commit_time
        elif l.startswith("author"):
            author, author_time = parse_commiter_line(l)
            gi["author"] = author
            gi["author_date"] = author_time

    return gi

def get_git_info_dir(directory):
    head_commit = get_head_commit(directory)
    if not head_commit:
        return

    head_message_folder = head_commit[:2]
    head_message_filename = head_commit[2:]
    head_message_file = os.path.join(
        directory, "objects", head_message_folder, head_message_filename
    )
    
    gi = {"commit": head_commit, "gitdir": directory, "message": ""}

    if not os.path.isfile(head_message_file):
        # Here we open the snake bucket of idx+pack
        object_path = os.path.join(directory, "objects", "pack")
        for idx_file in glob.glob(object_path + "/*.idx"):
            get_pack_info(idx_file, gi)

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
