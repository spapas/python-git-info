# python-git-info

A very simple project to get information from the git repository of your project.
This package does not have any dependencies; it reads directly the data from the
.git repository.

## Installation

Just do a `pip install gitinfo`, or copy the `gitinfo/gitinfo.py` file to your
project directly. This project should work with both python 2.7 and 3.x.

## Usage

This app will search the current directory for a `.git` directory (which is
always contained inside the root directory of a project). If one is found
it will be used; else it will search the parent directory recursively until a
`.git` is found.

There's a single function name `get_git_info()` with an optional `dir` parameter.
If you leave it empty it will start the `.git` directory search from the current directory,
if you provide a value for `dir` it will start from that directory. The `get_git_info`
will return a dictionary with the following structure if everything works ok or
`None` if something fishy happend or no `.git` folder was found:

```
  {
    'parent_commit': 'd54743b6e7cf9dc36354fe2907f2f415b9988198', 
    'message': 'commit: Small restructuring\n', 
    'commiter': 'Serafeim <email@email.com>', 
    'commit_time': '2018-11-14 13:52:34', 
    'commit': '9e1eec364ad24df153ca36d1da8405bb6379e03b'
  }
```

## How it works

This project will return the info from the latest commit of your *current* branch. To do this, it will read the `.git/HEAD` file which contains your current branch (i.e something like `ref: refs/heads/master`). It will then read the file `.git/logs/ + current_head` i.e something like `.git/logs/refs/heads/master` which contains all the history of your current branch and retrieve the *last* line of that file which actually is the current changeset. This line has the following format: `parent-changeset current-changeset commiter unix-epoch-datetime<TAB>commit-message`, something like `2f038260609c15e86bcd8b3cef7b9ae9948e83f8 dea9676f779dbf487be88d9cd363de63c215e88f Serafeim Papastefanos <spapas@gmail.com> 1542266248 +0200     commit: Make it work with rel path`. 

To parse this, it splits first by <TAB> to get the commit message and then it splits the first part by space to retrieve the rest of the information.

## Rationale

This project may seem useless of very useful, depending on the way you deploy to your servers. If you, like me, push every changeset to your VCS *before* deploying and then pull the changes from the remote server to actually deploy then you'll find this project priceless: You can easily add the latest commit information to somewhere in your web application so you'll be able to see immediately which changeset is deployed to each server without the need to actually login to the server and do a `git log`.

## Changes

0.4

* Add more error checks

0.3

* Make it work with '..'

0.2

* Initial

