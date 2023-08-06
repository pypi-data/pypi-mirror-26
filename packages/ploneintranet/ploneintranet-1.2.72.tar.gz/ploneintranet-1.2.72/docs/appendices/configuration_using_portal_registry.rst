.. _configuration_using_portal_registry.rst:

===================================
Configuration using portal_registry
===================================

Plone intranet can be controlled by modifying the portal_registry.

The following registry records have beein configured through
the ploneintranet packages


ploneintranet.layout
--------------------

ploneintranet.layout.splashpage_enabled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Turn on the display of a first time splash page

    **description**: If the user logs in for the first time, he will see a splash page overlay which can contain introductory information stored in splashpage_content.

    **type**: plone.registry.field.Bool

    **default**: False

ploneintranet.layout.splashpage_uid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Configure a unique identifier for the splash page

    **description**: This UID is used to store the information in the user's browser if the splashpage has been shown already. If you want to make the splashpage reappear for all users, change the UID.

    **type**: plone.registry.field.TextLine

    **default**: ''

ploneintranet.layout.splashpage_content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Content of the splashpage

    **description**: This is the complete html markup used to render the splashpage.

    **type**: plone.registry.field.Text

    **default**: ''


ploneintranet.layout.dashboard_activity_tiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: List of dashboard activity tiles

    **description**: This is the list of the tiles the user will see on the "Activity centric view" dashboard.

    **type**: plone.registry.field.Tuple composed of plone.registry.field.TextLine

    **default**: ./@@contacts_search.tile,
                 ./@@bookmarks.tile?id_suffix=-dashboard
                 ./@@news.tile,
                 ./@@my_documents.tile

ploneintranet.layout.dashboard_task_tiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: List of dashboard activity tiles

    **description**: This is the list of the tiles the user will see on the "Task centric view" dashboard.

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: ./@@contacts_search.tile,
                 ./@@news.tile,
                 ./@@my_documents.tile,
                 ./@@workspaces.tile?workspace_type=ploneintranet.workspace.workspacefolder,
                 ./@@workspaces.tile?workspace_type=ploneintranet.workspace.case,
                 ./@@events.tile,
                 ./@@tasks.tile,

ploneintranet.layout.dashboard_custom_tiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: List of dashboard custom tiles

    **description**: This is the list of the tiles the user will see on the "My view (customizable)" dashboard.

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: './@@contacts_search.tile?title=Contacts',
                 './@@news.tile?title=News',
                 './@@my_documents.tile?title=My docs',

ploneintranet.layout.dashboard_default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Name of the default dashboard

    **description**: This is the name of the dashboard type that should be shown by default. Pick the values from the dropdown on the dashboard.

    **type**: plone.registry.field.TextLine

    **default**: activity


ploneintranet.layout.login_splash
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Splash image for the login form

    **description**: This is the path, relative to the portal url, used to customize the login_form splash image

    **type**: plone.registry.field.TextLine

    **default**: ++theme++ploneintranet.theme/generated/media/logos/plone-intranet-square-dp.svg


ploneintranet.layout.filter_news_by_published_state
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Filter news in portlet by published state

    **description**: When set to true (default), the news portlet will only search for items in workflow state published. You can turn that off to become more flexible in controlling the search by actual view permissions. This can come in handy when you use different published states.

    **type**: plone.registry.field.Bool

    **default**: True


ploneintranet.layout.custom_bubbles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Custom help bubbles

    **description**: Specify custom help bubbles in a json format, e.g.: {"foo-bar": {"title": "Foo", "description": "<p>Bar baz</p>"}}  (this may change in the future)

    **type**: plone.registry.field.Text

    **default**: None


ploneintranet.layout.bubbles_enabled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Enable the help bubbles

    **description**: Setting this value to "On" will show the help bubbles unless the user disables them. Setting this value to "Off" will not show the help bubbles unless the user enables them. Setting this value to "Disabled": will deactivate the help bubbles feature.

    **type**: plone.registry.field.Choice (plone.registry.field.TextLine)

    **default**: Off


ploneintranet.library
---------------------

ploneintranet.library.order_by_modified
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Re-order library folder after publishing widely

    **description**: If True (default), a library folder will be re-ordered so that the item modified last is on top every time a "Publish widely" action happens.

    **type**: plone.registry.field.Bool

    **default**: True


ploneintranet.docconv.client
----------------------------


ploneintranet.docconv.file_types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Preview Content Types

    **description**: Generate preview images directly from this list of content types

    **type**: plone.registry.field.TextLine

    **default**: File

ploneintranet.docconv.html_types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: HTML Preview Content Types

    **description**: Generate preview images from PDF versions of this list of content types

    **type**: plone.registry.field.TextLine

    **default**: Document

ploneintranet.docconv.num_previews
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Number of previews generated

    **description**: Limit the number of previews generated by default. This protects the system against PDFs with 35.000 pages.

    **type**: plone.registry.field.Int

    **default**: 20


ploneintranet.search
--------------------

ploneintranet.search.filter_fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Filter fields

    **description**: Fields that will be used to filter query responses in searches

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: tags,
                 friendly_type_name,
                 portal_type,
                 path,
                 is_division,
                 division


ploneintranet.search.facet_fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Facet field

    **description**: A field that will be used to facet query responses

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: tags,
                 friendly_type_name,
                 is_division,


ploneintranet.search.phrase_fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Phrase fields

    **description**: Fields to which the main search phrase will be applied

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: Title,
                 Description,
                 tags,
                 SearchableText


ploneintranet.search.solr.phrase_field_boosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Phrase query field and associated boost values

    **description**: Solr Boost values used to compute relevency for queries.

    **type**: plone.registry.field.Dict {plone.registry.field.TextLine: plone.registry.field.Int}

    **default**: Title: 5
                 Description: 3
                 tags: 4
                 SearchableText: 1

    **note**: minimum accepted integer is 1


ploneintranet.search.ui.persistent_options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Persistent search options

    **description**: If this option is enabled, the selected search options will be stored for every user

    **type**: plone.registry.field.Bool

    **default**: False


ploneintranet.search.ui.additional_facets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Additional facets for filtering your results

    **description**: The search results page, by default,
                     facets the search results using the friendly_type_name field.
                     Here you can list additional fields you want to use for faceting.
                     Each field should be specified as field
                     (should match the values from ploneintranet.search.facet_fields)
                     and label
                     (a value that can be translate in the ploneintranet 18n domain)

    **type**: plone.registry.field.Dict {plone.registry.field.ASCII: plone.registry.field.TextLine}

    **default**: {'tags': 'Tags'}


ploneintranet.userprofile
-------------------------

ploneintranet.userprofile.hidden_fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Hidden fields

    **description**: User profile fields that are hidden from the profile editing page

    **type**: plone.registry.field.Tuple composed of plone.registry.field.TextLine

    **default**:

ploneintranet.userprofile.property_sheet_mapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Property sheet mapping

    **description**: A mapping of a user property to a specific
                     property sheet which
                     should be used to obtain the data for this attribute.

    **type**: plone.registry.field.Dict {plone.registry.field.ASCII: plone.registry.field.TextLine}

    **default**:

ploneintranet.userprofile.primary_external_user_source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Primary External User Source

    **description**: The ID of the PAS plugin that will be treated as the primary source of external users.

    **type**: plone.registry.field.ASCIILine

    **default**:

ploneintranet.userprofile.read_only_fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Read only fields

    **description**: User profile fields that are read-only
                    (shown on profile editing page but not editable)

    **type**: plone.registry.field.Tuple composed of plone.registry.field.TextLine

    **default**: username

ploneintranet.userprofile.locations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Hidden fields

    **description**: User profile fields that are hidden from the profile editing page

    **type**: plone.registry.field.Tuple composed of plone.registry.field.TextLine

    **default**: London,
                 Amsterdam,
                 Berlin,
                 Paris,
                 New York


ploneintranet.workpace
----------------------

ploneintranet.workspace.allow_bulk_subscribe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**title**: Allow the subscribe bulk action

**description**: If set to True, the user can subscribe to the selected objects

**type**: plone.registry.field.Bool

**default**: True


ploneintranet.workspace.case_manager.states
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Case Manager Workflow States

    **description**: Only these States are shown for filtering

    **type**: plone.registry.field.Tuple composed of plone.registry.field.TextLine

    **default**: new, pending, published, rejected

ploneintranet.workspace.externaleditor_always_activated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: External Editor always activated.

    **description**: When true, the isActivatedInMemberProperty()
                     and isActivatedInSiteProperty()
                     methods of the EnabledView always return True.
                     Otherwise the normal behaviour as implemented
                     in collective.externaleditor is used.

    **type**: plone.registry.field.Bool

    **default**: False

ploneintranet.workspace.sort_options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Workspace sort options

    **description**: Controls in which way we are able to sort the workspaces

    **type**: plone.registry.field.Dict {plone.registry.field.TextLine: plone.registry.field.TextLine}

    **default**:  activity: Most active workspaces on top
                  alphabet: Alphabetical
                  newest: Newest workspaces on top

ploneintranet.workspace.my_workspace_sorting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: My workspace sorting.

    **description**: At the moment we are able to handle the values "active", "alphabet" and "newest".

    **type**: plone.registry.field.TextLine

    **default**: alphabet

ploneintranet.workspace.workspace_types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Select workspace types

    **description**: Only this types are searched when looking for workspaces

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: ploneintranet.workspace.workspacefolder,
                 ploneintranet.workspace.case

    **note**: this will probably removed in favour of filtering
              by interface

ploneintranet.workspace.workspace_types_css_mapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Maps workspace portal types to css classes

    **description**: If a portal_type is not here it will default to regular.
                     The values should be passed as "{type}|{css class}",
                     e.g. "ploneintranet.workspace.case|type-case"

    **type**: plone.registry.field.Tuple of plone.registry.field.TextLine

    **default**: ploneintranet.workspace.case|type-case


ploneintranet.workspace.sanitize_html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Sanitize HTML on saving.

    **description**: If set to True, RichText content (HTML) in workspaces is sanitized before it gets stored. That means all open tags are properly closed, and inline styles and unwanted tags such as ``<span>`` or ``<blockquote>`` get stripped. Multipe line breaks get reduced to a single line break.

    **type**: plone.registry.field.Bool

    **default**: True


ploneintranet.workspace.autosave_portal_types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Autosave portal types

    **description**: Enable autosave for the selected portal types (works for edit forms inside workspaces)

    **type**: plone.registry.field.Tuple composed of plone.registry.field.TextLine

    **default**: []


ploneintranet.workspace.autosave_delay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Autosave delay

    **description**: Number of ms the client will wait before submitting a document

    **type**: plone.registry.field.Int

    **default**: 2000


ploneintranet.workspace.use_phase_due_dates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Use Phase Due Dates.

    **description**: If set to True, cases will expose the due date management functionality. You need to have the quaive.app.milestones package installed.

    **type**: plone.registry.field.Bool

    **default**: False


ploneintranet.workspace.phase_due_dates_default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    **title**: Default Value for Phase Due Dates.

    **description**: If set to True, workspaces will be created with due date support turned on by default. You need to have the quaive.app.milestones package installed.

    **type**: plone.registry.field.Bool

    **default**: False
