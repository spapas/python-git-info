import time


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


def parse_git_message(data, gi):
    lines = data.decode("utf-8").split("\n")
    reading_pgp = False
    reading_msg = False
    for idx, l in enumerate(lines):
        if l == "" and not reading_msg:
            reading_pgp = False
            reading_msg = True
            continue

        if reading_pgp == True:
            continue

        if reading_msg == True:
            gi["message"] += l
            if not l and idx < len(lines)-1:
                gi['message']+='\n'

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
