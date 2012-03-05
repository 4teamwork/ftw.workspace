Introduction
============

``ftw.workspace`` provides a project folder for plone.

The folder has a tabbed view with the tabs:

- **Overview**: Shows recently modified contents within this workspace and the structure (subfolders)
- **Documents**: Lists files recursively
- **Events**: Lists events (see ``ftw.meeting``) and a calendar view.

The ``@@workspaces_view`` lists all workspaces recursively.


Usage
=====

- Install the package by adding it to your buildout configuration:

::

    [instance]
    eggs =+
        ftw.workspace

- Install the generic setup profile.


Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.workspace
- Issue tracker: https://github.com/4teamwork/ftw.workspace/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.workspace
- Continuous integration: https://jenkins.4teamwork.ch/job/ftw.workspace/


Maintainer
==========

This package is produced and maintained by `4teamwork <http://www.4teamwork.ch/>`_ company.



.. _ftw.meeting: https://github.com/4teamwork/ftw.meeting
