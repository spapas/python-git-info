import os
import time


def find_git_dir(dir):
    absdir = os.path.abspath(dir)
    gitdir = os.path.join(absdir, ".git")
    if os.path.isdir(gitdir):
        return gitdir
    parentdir = os.path.dirname(absdir)
    if absdir == parentdir:
        # We reached root and found not gitdir
        return None
    return find_git_dir(parentdir)


def get_git_info_dir(dir):
    head_file = os.path.join(dir, "HEAD")
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
    log_file = os.path.join(dir, "logs", *head_parts)
    if not os.path.isfile(log_file):
        return
    last_line = None
    with open(log_file, "r") as fl:
        gi = {}
        for line in fl:
            last_line = line
        ll_parts = last_line.strip().split("\t")
        gi["message"] = ll_parts[1]
        ll_parts2 = ll_parts[0].split()
        gi["parent_commit"] = ll_parts2[0]
        gi["commit"] = ll_parts2[1]
        unix_time = float(ll_parts2[-2])
        # tz = ll_parts2[-1]
        gi["commiter"] = " ".join(ll_parts2[2:-2])
        gi["commit_time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(unix_time)
        )
        gi["gitdir"] = dir
        # TODO: I'll ignore tz for now

        return gi


def get_git_info(dir=os.getcwd()):
    gitdir = find_git_dir(dir)
    if not gitdir:
        return None
    return get_git_info_dir(gitdir)


if __name__ == "__main__":
    print(get_git_info())
