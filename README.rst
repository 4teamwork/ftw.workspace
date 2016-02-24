Introduction
============

``ftw.workspace`` provides a full featured project folder for Plone.

It uses ``ftw.tabbedview`` and ``ftw.activity`` to give you a overview view what happens
in your project.

What could happen in your project you're asking?

- Share files
    - Multi-upload using `collective.quickupload` - You are able to directly drop files into the Workspace, the Quickupload portlet is not necessary.
    - `ftw.file` provides a journal, versions, D'n'D file replacement, and much more.
    - Seperate Tabs, which shows all files, including filtering and Image preview.
- Manage your Team.
    - Extend your Team with ``ftw.participation``. Invite external an internal people to collaborate.
    - Overview of who is collaborating and open invitations.
- Meetings and Events
    - Add Meetings or Events.
    - Overview of all Meetings and Events as list or FullCalendar using ``ftw.calendar``.
- General features
    - Download all necessary informations of the Workspace as PDF.
    - Once you're done with the Project you can Download everything as ZIP-File.
    - Shows activities (Add, Modify, Delete, etc.)
    - Uploaded something interesting? Notify the People you want with ``ftw.notification``.
    - All Informations are fast accessible thru Tabs.
    - Create Project structures with Folders.
    - Global Overview of all your Projects with the ``@@workspaces_view``.
    - Using ExtJS for tabular listings.
    - Move and delete files directly in listings.



Integrated AddOns
-----------------
**``egov.contactdirectory``** is implemented as `extras`::


    [instance]
    eggs =+
        ftw.workspace [contact]


An additional profile is implemented which adds a new Tab to the Workspace and make the Contacts addable.


**PDF generation** is implemented as `extras`::

    [instance]
    eggs =+
        ftw.workspace [pdf]

Consider not installing it, if PDFLatex binaries are missing.


Possible AddOns
---------------
You may extend the Workspace by the following features.

- ``izug.ticketbox``
- ``ftw.mail``
- ``ftw.book``
- ``ftw.blog``
- ``ftw.contentpage``
- ``ftw.labels``
- ``ftw.downloadtoken``
- ``ftw.quota``
- ``ftw.avatar``



Example Workflow
================
``ftw.workspace`` is shipped with a ``ftw.lawgiver`` based default workflow for Workspaces.
You need to copy the workflow specifications of all three workflows (incl. placeful workflow policy) to your policy package and generate the necessary definition.xml using ftw.lawgiver. Check ``ftw.lawgiver`` for further informations.
You may also update the placeful workflow mappings with other types used in Workspaces.


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

- Github: https://github.com/4teamwork/ftw.workspace
- Issues: https://github.com/4teamwork/ftw.workspace/issues
- Pypi: http://pypi.python.org/pypi/ftw.workspace
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.workspace


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.workspace`` is licensed under GNU General Public License, version 2.


.. _ftw.meeting: https://github.com/4teamwork/ftw.meeting
