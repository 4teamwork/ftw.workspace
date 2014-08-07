Introduction
============

``ftw.workspace`` provides a project folder for plone.

The folder has a tabbed view with the tabs:

- **Overview**: Shows recently modified contents within this workspace and the structure (subfolders)
- **Documents**: Lists files recursively
- **Events**: Lists events (see ``ftw.meeting``) and a calendar view.

The ``@@workspaces_view`` lists all workspaces recursively.


Compatibility
=============

``ftw.workspace`` Version 2.0.0 and greater only supports Plone 4.3.x

Use ``ftw.workspace`` Version 1.7.x for Plone 4.1 and Plone 4.2.


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
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.workspace


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.workspace`` is licensed under GNU General Public License, version 2.


.. _ftw.meeting: https://github.com/4teamwork/ftw.meeting

.. image:: https://cruel-carlota.pagodabox.com/58be9c0bedbcc0b1f4df6ac60b428464
   :alt: githalytics.com
   :target: http://githalytics.com/4teamwork/ftw.workspace
