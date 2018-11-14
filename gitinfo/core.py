import os, time


def find_git_dir(dir):
    gitdir = os.path.join(dir, ".git")
    if os.path.isdir(gitdir):
        return gitdir
    parentdir = os.path.dirname(dir)
    if dir == parentdir:
        # We reached root and found not gitdir
        return None
    return find_git_dir(parentdir)

def get_git_info(dir):
    head_file = os.path.join(dir, "HEAD")
    head_parts = None
    with open(head_file, "r") as fh:
        data = fh.read().strip()
        head_parts = data.split(' ')[1].split('/')
    if not head_parts:
        return
    log_file = os.path.join(dir, 'logs', *head_parts)
    last_lane = None
    with open(log_file, "r") as fl:
        for line in fl:
            last_line = line
        ll_parts = last_line.split('\t')
        message = ll_parts[1]
        ll_parts2 = ll_parts[0].split()
        parent_commit = ll_parts2[0]
        commit = ll_parts2[1]
        unix_time = float(ll_parts2[-2])
        tz = ll_parts2[-1]
        commiter = ' '.join(ll_parts2[2:-2])

        normal_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_time))
        print commiter, normal_time

def start():
    gitdir = find_git_dir(os.getcwd())
    if not gitdir:
        print("Could not find gitdir")
    else:
        print("Found git dir at {0}".format(gitdir))

    get_git_info(gitdir)


if __name__ == "__main__":
    start()
