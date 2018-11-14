# django-git-info

A very simple app to get informatin from the git repository of your project.

**Warning: You must have git 2.6+ installed in order to use this application.** This version of git adds a custom format for date, which is required in order to parse the dates in python.

Just add a ``DJANGO_GIT_REPO = REPO_DIR`` setting to your settings.py - ``BASE_DIR``
is where your git repository resides - usually this should be in the same directory
as your ``manage.py``.

After that, you can immediately get information about your git repo using 
the ``get_git_info`` function:

```

from django_git_info import get_git_info

info = get_git_info()

print info['hash']

```

The keys of the returned dictionary are:
hash,  abbr_hash,  subject, sanitized_subject,  body,  author_name,  author_email,
author_date,  commiter_name,  commiter_email, commiter_date - check out what each
one does at: https://git-scm.com/docs/pretty-formats


Also, there's a JSON view to get your git info from an API - just add the
following to your urls.py:

```
from django_git_info.views import git_info

urlpatterns = [
    ...
    url(r'^git_info/$', git_info),
]
```

Also, if you want to print the git info to other views, there's a templatetag for this.
Just include ``django_git_info`` to your ``INSTALLED_APPS`` setting and in your templates you
could do:

```
{% load django_git_info_tags %}
{% get_git_info as gi %}

<ul>
    <li>Hash: {{ gi.hash }}</li>
    <li>Subject: {{ gi.subject }}</li>
    <li>Commiter date: {{ gi.commiter_date }}</li>
</ul>

```

Finally, there's also a ``get_git_info`` management command to ensure that everything
will going to work ok: 

```
> python manage.py get_git_info

body=
commiter_date=2016-03-06T15:10:00
hash=8d4f55cc2f7ff86b2ed7679e9252ae02cb360039
commiter_name=serafeim
...
```

