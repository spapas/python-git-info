# python-git-info

A very simple project to get information from the git repository of your project.
This package does not have any dependencies; it reads directly the data from the
.git repository.

## Installation

Just do a `pip install gitinfo`, or copy the gitinfo/gitinfo.py file to your
project directly.

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

## Changes

0.3

* Make it work with '..'

0.2

* Initial

