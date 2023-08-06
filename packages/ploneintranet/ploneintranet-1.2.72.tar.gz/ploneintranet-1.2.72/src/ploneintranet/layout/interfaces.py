# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from plone.app.event.interfaces import IBrowserLayer as IPloneAppEventLayer
from plone.app.z3cform.interfaces import IPloneFormLayer
from zope.interface import Attribute
from zope.interface import Interface


# NB additional content interfaces in .app.

class IPloneintranetLayoutLayer(Interface):
    """Marker interface for ploneintranet.layout installed"""


class INoBarcelonetaLayer(Interface):
    """Layer that is not active in Barceloneta"""


class IPloneintranetContentLayer(IPloneAppContenttypesLayer,
                                 IPloneAppEventLayer):
    """ Subclass the browserlayer of p.a.c and p.a.e to override the views.
    """


class IPloneintranetFormLayer(IPloneFormLayer):
    """ Request layer installed via browserlayer.xml

        z3c.form forms are rendered against this layer.
    """


class IAppLayer(Interface):
    """
    Mixin for browser layer to mark a Zope 3 browser layer as only
    being applicable within a specific IAppContainer
    """


class IAppContainer(Interface):
    """
    Mixin for content interface to mark a content object in which
    a specific IAppLayer should be activated on traversal.

    The implementer will typically also be an app.IApp.

    NOT to be confused with the app.IAppsContainer toplevel singleton.
    """

    app_name = Attribute("Name of the app. Will be set as app-{name} on body.")
    app_layers = Attribute("A list of IAppLayer to be activated on traversal")


class IDiazoNoTemplate(Interface):
    """
    Views marked by this interface will receive a "diazo off" class
    that will skip diazo transforms
    """


class IModalPanel(IDiazoNoTemplate):
    """
    Views marked by this interface will receive a "diazo off modal-panel" class
    that will skip diazo transforms nad will render nicely the panel
    """


class IDiazoAppTemplate(Interface):
    """
    Views marked by this interface will receive a diazo-template-* class
    that can be used in diazo transforms
    """


class IAppView(IDiazoAppTemplate):
    """
    View interface to mark a view as being placed within the Apps section.
    I.e. event app views on the siteroot that don't have an IAppManager
    context can be rendered 'within' the Apps section.
    """
    app_name = Attribute("Name of the app. Will be set as app-{name} on body.")


class IAppContent(Interface):
    """
    Adapter interface for content that is (possibly) contained within an
    IAppContainer, including nested content deep in a tree.
    """

    app_name = Attribute("Name of the app this content is contained in. "
                         "Returns: string, or empty string if not contained.")

    in_app = Attribute("Is this content contained within an IAppContainer? "
                       "Returns: boolean.")

    def get_app():
        """
        Return the IAppContainer this content is contained in, or None.
        """
