from zope.interface import Interface


class IWorkspace(Interface):
    """A type for collaborative spaces."""


class ITabbedViewFolder(Interface):
    """Tabbed view folder marker interface.
    """


class IWorkspaceDetailsListingProvider(Interface):
    """A adapter providing a listing (LaTeX) for the workspace details PDF.
    """

    def __init__(context, request, layout, view):
        """Adapts context, request, layout and view.
        """

    def get_title():
        """Returns the title of the listing (LaTeX).
        """

    def get_listing():
        """Returns the complete listing (LaTeX).
        """

    def get_sort_key():
        """A integer number which is used for sorting the listings.
        Small numbers are at the top, big numbers at the bottom.
        """


class IWorkspaceLayer(Interface):
    """Request marker interface for ftw.workspace"""


class IWorkspacePreview(Interface):
    """Generic preview adapter"""

    def __init__(context, request):
        """Adapts context and request"""

    def preview():
        """Renders the preview, usually an image"""

    def full_url():
        """URL of the image showing the large scale"""

    def get_scale_properties():
        """Returns the scale defined in configuration registry"""
