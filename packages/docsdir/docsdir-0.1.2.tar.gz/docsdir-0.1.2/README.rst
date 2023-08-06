docsdir
=======

This application is not a server. It is meant to run as a daemon under linux environment. Purpose of it is to watch for changes in a directory where you store documentation of your projects. In case of any change, relevant files in repository are updated automatically. It is best to explain this on an example. Docsdir assumes following structure of your repository:

.. code-block:: none

    repo/
    project_x/
        1.0.1/
        1.0.3/
        1.2.3/
        downloads/
        latest/
        index.html.jinja
        index.html
    project_y/
        (...)
    project_z/
        (...)
    _static/
    index.html.jinja
    index.html
    (...)

There are following types of directories:

* Top most directory
    It is the one where you store directories with your projects. Directories that starts with underscore `_` are ignored. This directory can contain .jinja files which will be used as templates for generating corresponding files without .jinja extension every time when you add/remove/move project directories.

* Project directory
    This one is meant to contain version directories (named according to semver convention) and other project-related directories as well as .jinja files which are used to generate static content whenever you add/remove/move version directories. Note that docsdir also maintains ``latest/`` symlink which points to the directory with the most recent version of your documentation.

* Version directory
    Directory of this kind is meant to contain documentation of your project, but it can contain anything that you like. It is not inspected by docsdir.

Syntax:

.. code-block:: none

    python3 -m docsdir [REPO_PATH [GUARD_TIME]]
        REPO_PATH - path to the repo, default=./repo
        GUARD_TIME - time in seconds after the last repository update that the tool waits before regeneration begins, default=1

Notes:

* Docsdir doesn't serve files from repository over HTTP. Another tool (Apache, Nginx, etc.) can be used for that.
* Docsdir doesn't maintain user accounts. Linux itself can be used for limiting access rights of the project owners.
