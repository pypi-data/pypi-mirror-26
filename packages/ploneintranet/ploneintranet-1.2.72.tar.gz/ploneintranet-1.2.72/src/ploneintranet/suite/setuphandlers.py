# -*- coding: utf-8 -*-
from collective.workspace.interfaces import IWorkspace
from datetime import date
from datetime import datetime
from datetime import timedelta
from plone import api
from plone.app.event.base import localized_now
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobImage
from ploneintranet import api as pi_api
from ploneintranet.docconv.client.decorators import force_synchronous_previews
from ploneintranet.microblog.interfaces import IMicroblogTool
from ploneintranet.microblog.migration import discuss_older_docs
from ploneintranet.network.behaviors.metadata import IDublinCore
from ploneintranet.network.interfaces import INetworkTool
from ploneintranet.news.content import INewsApp
from ploneintranet.workspace.config import TEMPLATES_FOLDER
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import Invalid

import copy
import csv
import json
import logging
import loremipsum
import os
import pytz
import random
import re
import time


log = logging.getLogger(__name__)

# commits are needed in interactive but break in test mode
if api.env.test_mode:
    def commit():
        return
else:
    from transaction import commit


def default(context):
    """Run when installing the default profile.
    """
    log.info("create case templates")
    casetemplates = case_templates_spec(context)
    # TEMPLATES_FOLDER is already created by ploneintranet.workspace
    create_caseworkspaces(casetemplates, container=TEMPLATES_FOLDER)
    log.info("publish top-level portal sections / apps")
    portal = api.portal.get()
    pwt = api.portal.get_tool('portal_workflow')
    to_publish = ('news', 'library', 'apps', 'profiles')
    for id in to_publish:
        obj = getattr(portal, id, None)
        if obj and api.content.get_state(obj) != 'published':
            try:
                pwt.doActionFor(obj, 'publish')
            except:
                log.exception('Cannot publish the top-level item: %r', obj)
    commit()

    log.info("default setup: done.")


def full(context):
    ''' Full profile also deletes default Plone content
    '''
    log.info("default setup")
    cleanup_default_content(context)
    commit()
    default(context)


def _setup_event_agenda_items():
    ''' We set up the agenda items field in a test event.

    The agenda items will be composed of one UID and three normal strings
    '''
    folder = api.content.get(
        '/workspaces/open-market-committee/manage-information'
    )
    event = folder['open-market-day']
    document = folder['repurchase-agreements']
    event.agenda_items = [
        'Prologue',
        document.UID(),
        u'☰',
        u'Epilogue and final greetings',
    ]


@force_synchronous_previews
def testing(context):
    """
    Important!
    We do not want to have users with global roles such as Editor or
    Contributor in our test setup.
    """
    log.info("testcontent setup")
    context = context._getImportContext(
        'profile-ploneintranet.suite:testing')

    log.info("create_users")
    users = users_spec(context)
    create_users(context, users, 'avatars')
    commit()

    log.info("create workspaces")
    workspaces = workspaces_spec(context)
    create_workspaces(workspaces)
    commit()

    log.info("create caseworkspaces")
    caseworkspaces = caseworkspaces_spec(context)
    create_caseworkspaces(caseworkspaces)
    _setup_event_agenda_items()
    commit()

    portal = api.portal.get()
    # big setup only when manually re-running testcontent
    bigsetup = bool(len(portal.library.objectIds()))
    log.info("create library content, bigsetup=%s", bigsetup)
    library = library_spec(context)
    # will create minimal library with only small HR section by default
    # will create big library on second manual testcontent run
    # will do nothing on third and subsequent runs
    create_library_content(None, library, bigsetup=bigsetup)
    commit()

    log.info("create microblog stream")
    stream_json = os.path.join(context._profile_path, 'stream.json')
    with open(stream_json, 'rb') as stream_json_data:
        stream = json.load(stream_json_data)
    create_stream(context, stream, 'files')
    commit()

    log.info("add discussion streams on testcontent")
    # easier than emitting event and running into async issues
    discuss_older_docs(None, do_commit=False)
    commit()  # no-op when in test mode avoids breakage

    log.info("Create some bookmarks")
    create_bookmarks()
    commit()

    log.info("Create direct messages")
    create_messages()
    commit()

    # ploneintranet.news test content is setup by news:testing
    log.info("Grant editor access to news app")
    configure_news()
    commit()

    log.info("done.")


def cleanup_default_content(context):
    """ Remove default content created by Plone for an empty site,
        we don't need it. """

    log.info('cleanup Plone default content')
    portal = api.portal.get()
    delete_ids = ['front-page', 'events', 'Members']
    # if the News App has already been created, don't delete it here again
    if 'news' in portal:
        app_obj = portal.news
        if not INewsApp.providedBy(app_obj):
            delete_ids.append('news')
    default_content = [portal.get(c) for c in delete_ids
                       if c in portal.objectIds()]
    if default_content:
        api.content.delete(objects=default_content)
        log.info('removed Plone default content')
    else:
        log.info('no Plone default content to remove')


def users_spec(context):
    users_csv_file = os.path.join(context._profile_path, 'users.csv')
    users = []
    with open(users_csv_file, 'rb') as users_csv_data:
        reader = csv.DictReader(users_csv_data)
        for user in reader:
            user = {
                k: v.decode('utf-8') for k, v in user.iteritems()
            }
            if not user.get('email', '').strip():
                user['email'] = '{}@example.com'.format(decode(user['userid']))
            user['follows'] = [
                decode(u) for u in user['follows'].split(' ') if u
            ]
            users.append(user)
    return users


def create_users(context, users, avatars_dir, force=False):
    """Creates user from the given list of dictionaries.

    ``context`` is the step context.

    ``users`` is a list of dictionaries each containing the following keys:

      * userid
      * fullname
      * email
      * location
      * description
      * follows (a list of userids followed)

    ``avatars_dir`` is a directory where for each userid
    there is a ``$userid.jpg`` file.
    """
    for i, user in enumerate(users):
        email = decode(user['email'])
        userid = decode(user['userid'])
        portrait_filename = '{}.jpg'.format(userid)
        fullname = user.get('fullname', u"Anon Ymous {}".format(i))
        firstname, lastname = fullname.split(' ', 1)
        properties = {
            'fullname': fullname,
            'first_name': firstname,
            'last_name': lastname,
            'location': user.get('location', u"Unknown"),
            'description': user.get('description', u"")
        }
        try:
            profile = pi_api.userprofile.create(
                username=userid,
                email=email,
                password='secret',
                approve=True,
                properties=properties,
            )
            log.info('Created user {}'.format(userid))
        except Invalid:
            # Already exists

            if not force:
                log.info("users already configured. skipping for speed")
                return

            # update
            profile = pi_api.userprofile.get(userid)
            for key, value in properties.items():
                if key != 'fullname':  # now this field is calculated
                    setattr(profile, key, value)
            log.info('Updated user {}'.format(userid))

        portrait_path = os.path.join(avatars_dir, portrait_filename)
        portrait = context.openDataFile(portrait_path)
        if portrait:

            image = NamedBlobImage(
                data=portrait.read(),
                filename=portrait_filename.decode('utf-8'))
            profile.portrait = image
        else:
            log.warning(
                'Missing portrait file for {}: {}'.format(
                    userid,
                    portrait_filename
                )
            )

    # setup social network
    graph = queryUtility(INetworkTool)
    graph.clear()
    for user in users:
        for followee in user.get('follows', []):
            graph.follow("user", decode(followee), user['userid'])


def workspaces_spec(context):
    now = localized_now()
    budget_proposal_filename = u'budget-proposal.png'
    budget_proposal_path = os.path.join('images', budget_proposal_filename)
    budget_proposal_img = NamedBlobImage(
        data=context.openDataFile(budget_proposal_path).read(),
        filename=budget_proposal_filename
    )
    minutes_filename = u'minutes.docx'
    minutes_path = os.path.join('files', minutes_filename)
    minutes_file = NamedBlobImage(
        data=context.openDataFile(minutes_path).read(),
        filename=minutes_filename
    )

    tomorrow = (now + timedelta(days=1)).replace(hour=9, minute=0, second=0,
                                                 microsecond=0)
    next_month = (now + timedelta(days=30)).replace(hour=9, minute=0,
                                                    second=0, microsecond=0)

    # Create workspaces
    workspaces = [
        {'title': 'Open Market Committee',
         'description': 'The OMC holds eight regularly scheduled meetings '
                        'during the year and other meetings as needed.',
         'transition': 'make_private',
         'participant_policy': 'publishers',
         'members': {'allan_neece': [u'Members'],
                     'christian_stoney': [u'Admins', u'Members'],
                     'neil_wichmann': [u'Members'],
                     'francois_gast': [u'Members'],
                     'jamie_jacko': [u'Members'],
                     'jesse_shaik': [u'Members'],
                     'jorge_primavera': [u'Members'],
                     'silvio_depaoli': [u'Members'],
                     'lance_stockstill': [u'Members'],
                     'pearlie_whitby': [u'Members'],
                     'dollie_nocera': [u'Members'],
                     'esmeralda_claassen': [u'Members'],
                     'rosalinda_roache': [u'Members'],
                     'guy_hackey': [u'Members'],
                     },
         'contents':
             [{'title': 'Manage Information',
               'type': 'Folder',
               'contents':
                   [{'title': 'Preparation of Records',
                     'description': 'How to prepare records',
                     'state': 'published',
                     'subject': 'Read carefully',
                     'type': 'File',
                     },
                    {'title': 'Public bodies reform',
                     'description': 'Making arrangements for the transfer of '
                                    'information, records and knowledge is a '
                                    'key part of any Machinery of Government '
                                    'change.',
                     'type': 'Document',
                     'state': 'published'},
                    {'title': 'Repurchase Agreements',
                     'description': 'A staff presentation outlined several '
                                    'approaches to raising shortterm interest '
                                    'rates when it becomes appropriate to do '
                                    'so, and to controlling the level of '
                                    'short-term interest rates ',
                     'owner': 'allan_neece',
                     'type': 'Document'},
                    {'title': u'Budget Proposal',
                     'description': (
                         u'A diagram of the factors impacting the budget and '
                         u'results'
                     ),
                     'owner': 'allan_neece',
                     'image': budget_proposal_img,
                     'type': 'Image',
                     },
                    {'title': u'Minutes',
                     'owner': 'allan_neece',
                     'description': u'Meeting Minutes',
                     'file': minutes_file,
                     'type': 'File',
                     },
                    {'title': u'Minutes Overview',
                     'owner': 'allan_neece',
                     'description': u'Meeting Minutes Overview',
                     'type': 'Document',
                     'modification_date': now - timedelta(days=60),
                     },
                    {'title': 'Open Market Day',
                     'type': 'Event',
                     'state': 'published',
                     'start': tomorrow,
                     'end': tomorrow + timedelta(hours=8)},
                    {'title': 'Plone Conf',
                     'type': 'Event',
                     'state': 'published',
                     'start': next_month,
                     'end': next_month + timedelta(days=3, hours=8)},
                    {'title': "Yesterday's gone",
                     'type': 'Event',
                     'state': 'published',
                     'owner': 'allan_neece',
                     'start': tomorrow - timedelta(days=3),
                     'end': tomorrow - timedelta(days=2)},
                    ]},
              {'title': 'Projection Materials',
               'type': 'Folder',
               'contents':
                   [{'title': 'Projection Material',
                     'type': 'File'}]},
              {'title': 'Future Event',
               'type': 'Event',
               'start': now + timedelta(days=7),
               'end': now + timedelta(days=14)},
              {'title': 'Past Event',
               'type': 'Event',
               'start': now + timedelta(days=-7),
               'end': now + timedelta(days=-14)},
              {'title': 'Files for application 2837',
               'type': 'ploneintranet.workspace.mail',
               'mail_from': u'pilz@pilzen.de',
               'mail_to': (
                   u'open-market-committee@ourintranet.com',
                   u'cornelis@cornae.com',),
               'mail_body': RichTextValue(
                   u'''
                    <p>Dear mister Kolbach,</p>
                    <p>We’ll process your application with the shortest
                     delay.</p>
                    <p>Yours sincerely, <br>
                    Alexander Pilz</p>

                    <blockquote>
                      <p>Dear Sir or Madam,</p>

                      <p>Sed ut perspiciatis unde omnis iste natus error
                      sit voluptatem accusantium doloremque laudantium,
                      totam rem aperiam, eaque ipsa quae ab illo inventore
                      veritatis et quasi architecto beatae vitae dicta sunt
                      explicabo.</p>

                      <p>Kind regards,<br>
                    Cornelis G. A. Kolbach</p>
                    </blockquote>
                   '''
               ),
               'contents': [
                   {
                       'title': 'Budget proposal',
                       'type': 'Image',
                       'image': budget_proposal_img,
                   },
                   {
                       'title': u'Minutes',
                       'owner': 'allan_neece',
                       'description': u'Meeting Minutes',
                       'file': minutes_file,
                       'type': 'File',
                   },
               ]}
              ],
         },
        {'title': 'Parliamentary papers guidance',
         'description': '"Parliamentary paper" is a term used to describe a '
                        'document which is laid before Parliament. Most '
                        'government organisations will produce at least one '
                        'parliamentary paper per year.',
         'transition': 'make_private',
         'participant_policy': 'producers',
         'members': {'allan_neece': [u'Members'],
                     'christian_stoney': [u'Admins', u'Members'],
                     'francois_gast': [u'Members'],
                     'jamie_jacko': [u'Members'],
                     'fernando_poulter': [u'Members'],
                     'jesse_shaik': [u'Members'],
                     'jorge_primavera': [u'Members'],
                     'silvio_depaoli': [u'Members'],
                     'kurt_weissman': [u'Members'],
                     'esmeralda_claassen': [u'Members'],
                     'rosalinda_roache': [u'Members'],
                     'guy_hackey': [u'Members'],
                     },
         'contents':
            [{'title': 'Test Document',
              'description': 'A document just for testing',
              'type': 'Document'}]
         },
        {'title': u'Shareholder information',
         'description': u'"Shareholder information" contains all documents, '
            u'papers and diagrams for keeping shareholders informed about the '
            u'current state of affairs.',
         'transition': 'make_private',
         'participant_policy': 'consumers',
         'members': {'allan_neece': [u'Members'],
                     'christian_stoney': [u'Admins', u'Members'],
                     'francois_gast': [u'Members'],
                     'jamie_jacko': [u'Members'],
                     'fernando_poulter': [u'Members'],
                     'jesse_shaik': [u'Members'],
                     'jorge_primavera': [u'Members'],
                     'silvio_depaoli': [u'Members'],
                     'kurt_weissman': [u'Members'],
                     'esmeralda_claassen': [u'Members'],
                     'rosalinda_roache': [u'Members'],
                     'guy_hackey': [u'Members'],
                     },
         'contents':
            [{'title': 'Test Document',
              'description': 'A document just for testing',
              'type': 'Document',
              'state': 'published'}]
         },
        {'title': u'Service announcements',
         'description': u'Public service announcements can be found here.',
         'transition': 'make_open',
         'participant_policy': 'consumers',
         'members': {'allan_neece': [u'Members'],
                     'christian_stoney': [u'Admins', u'Members'],
                     'francois_gast': [u'Members'],
                     'jamie_jacko': [u'Members'],
                     'fernando_poulter': [u'Members'],
                     'jesse_shaik': [u'Members'],
                     'jorge_primavera': [u'Members'],
                     'silvio_depaoli': [u'Members'],
                     'kurt_weissman': [u'Members'],
                     'esmeralda_claassen': [u'Members'],
                     'rosalinda_roache': [u'Members'],
                     'guy_hackey': [u'Members'],
                     },
         'contents':
            [{'title': 'Terms and conditions',
              'description': 'A document just for testing',
              'type': 'Document',
              'state': 'published'},
             {'title': 'Customer satisfaction survey',
              'description': 'A private document',
              'type': 'Document'},
             ]
         },
    ]
    return workspaces


def create_workspaces(workspaces, force=False):
    portal = api.portal.get()
    ws_folder = portal['workspaces']

    if not force and ('ploneintranet.workspace.workspacefolder'
                      in [x.portal_type for x in ws_folder.objectValues()]):
        log.info("workspaces already setup. skipping for speed.")
        return

    for w in workspaces:
        contents = w.pop('contents', None)
        members = w.pop('members', {})
        transition = w.pop('transition', 'make_private')
        participant_policy = w.pop('participant_policy', 'consumers')
        workspace = api.content.create(
            container=ws_folder,
            type='ploneintranet.workspace.workspacefolder',
            **w
        )
        api.content.transition(obj=workspace, transition=transition)
        workspace.participant_policy = participant_policy
        if contents is not None:
            create_ws_content(workspace, contents)
        for (m, groups) in members.items():
            IWorkspace(workspace).add_to_team(user=m, groups=set(groups))


def case_templates_spec(context):
    today = date.today()
    case_templates = [{
        'title': 'Case Template',
        'description': 'A Template Case Workspace, pre-populated with tasks',
        'members': {'allan_neece': [u'Members'],
                    'dollie_nocera': [u'Members'],
                    'christian_stoney': [u'Admins', u'Members']},
        'contents': [{
            'title': 'Populate Metadata',
            'type': 'todo',
            'description': 'Identify and fill in the Metadata',
            'milestone': 'new',
        }, {
            'title': 'Identify the requirements',
            'type': 'todo',
            'description': 'Analyse the request and identify the requirements',
            'milestone': 'prepare',
        }, {
            'title': 'Draft proposal',
            'type': 'todo',
            'description': 'Create a draft proposal',
            'milestone': 'prepare',
            'creation_date': today - timedelta(days=2),
        }, {
            'title': 'Budget',
            'type': 'todo',
            'description': 'Propose funding',
            'milestone': 'prepare',
        }, {
            'title': 'Stakeholder feedback',
            'type': 'todo',
            'description': 'Collect initial stakeholder feedback',
            'milestone': 'prepare',
        }, {
            'title': 'Quality check',
            'type': 'todo',
            'description': 'Verify completeness of case proposal',
            'milestone': 'complete',
            'creation_date': today - timedelta(days=4),
        }, {
            'title': 'Financial audit',
            'type': 'todo',
            'description': 'Verify financial consequences',
            'milestone': 'audit',
        }, {
            'title': 'Legal audit',
            'type': 'todo',
            'description': 'Verify legal requirements',
            'milestone': 'audit',
        }, {
            'title': 'Schedule',
            'type': 'todo',
            'description': 'Schedule decision',
            'milestone': 'propose',
        }, {
            'title': 'Confirm',
            'type': 'todo',
            'description': 'Communicate decision to all stakeholders',
            'milestone': 'decided',
        }, {
            'title': 'Execute',
            'type': 'todo',
            'description': 'Implement decision taken',
            'milestone': 'decided',
        }, {
            'title': 'Evaluate',
            'type': 'todo',
            'description': 'Document post-implementation evaluation',
            'milestone': 'closed',
        }, {
            'title': 'File report',
            'type': 'todo',
            'description': 'Prepare case for archival',
            'milestone': 'closed',
        }],
    }]
    return case_templates


def caseworkspaces_spec(context):
    now = localized_now()
    today = date.today()
    # use template todos as a base
    base_contents = case_templates_spec(context)[0]['contents']
    for todo in base_contents:
        todo['initiator'] = 'christian_stoney'
    for i in range(2):
        base_contents[i]['state'] = 'done'
    for i in range(4):
        base_contents[i]['assignee'] = random.choice(['dollie_nocera',
                                                      'allan_neece'])
    for i in range(6):
        base_contents[i]['due'] = today + timedelta(days=i * 2)

    caseworkspaces = [{
        'title': 'Example Case',
        'description': 'A case management workspace demonstrating the '
                       'adaptive case management functionality.',
        'state': 'prepare',
        'members': {'allan_neece': [u'Members'],
                    'dollie_nocera': [u'Members'],
                    'christian_stoney': [u'Admins', u'Members']},
        'contents': base_contents + [{
            'title': 'Future Meeting',
            'type': 'Event',
            'start': now + timedelta(days=7),
            'end': now + timedelta(days=14)
        }, {
            'title': 'Past Meeting',
            'type': 'Event',
            'start': now + timedelta(days=-7),
            'end': now + timedelta(days=-14)
        }],
    }]
    return caseworkspaces


def create_caseworkspaces(caseworkspaces,
                          container='workspaces',
                          force=False,
                          workflow_policy='case_workflow',
                          portal_type='ploneintranet.workspace.case'):
    portal = api.portal.get()
    pwft = api.portal.get_tool("portal_placeful_workflow")

    if container not in portal:
        ws_folder = api.content.create(
            container=portal,
            type='ploneintranet.workspace.workspacecontainer',
            title='Workspaces'
        )
        api.content.transition(ws_folder, 'publish')
    else:
        ws_folder = portal[container]

    if not force and ('ploneintranet.workspace.case'
                      in [x.portal_type for x in ws_folder.objectValues()]):
        log.info("caseworkspaces already setup. skipping for speed.")
        return

    for w in caseworkspaces:
        contents = w.pop('contents', None)
        members = w.pop('members', [])
        state = w.pop('state', None)
        try:
            caseworkspace = api.content.create(
                container=ws_folder,
                type=portal_type,
                **w
            )
        except:
            log.exception(
                'Error creating %s in %r',
                portal_type,
                ws_folder,
            )
            continue

        caseworkspace.manage_addProduct[
            'CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        wfconfig = pwft.getWorkflowPolicyConfig(caseworkspace)
        wfconfig.setPolicyIn(workflow_policy)

        if contents is not None:
            create_ws_content(caseworkspace, contents)
        for (m, groups) in members.items():
            IWorkspace(
                caseworkspace).add_to_team(user=m, groups=set(groups))
        if state is not None:
            api.content.transition(caseworkspace, to_state=state)


def create_ws_content(parent, contents):
    for content in contents:
        sub_contents = content.pop('contents', None)
        owner = content.pop('owner', None)
        state = content.pop('state', None)
        obj = api.content.create(
            container=parent,
            **content
        )
        if owner is not None:
            try:
                api.user.grant_roles(
                    username=owner,
                    roles=['Owner'],
                    obj=obj,
                )
            except api.exc.InvalidParameterError, ipe:
                log.warning('Grant roles did not work for user %s. '
                            'Does the user exist?' % owner)
                raise api.exc.InvalidParameterError, ipe

            obj.reindexObject()
            # Avoid 'reindexObject' overriding custom
            # modification dates
            if 'modification_date' in content:
                obj.modification_date = content['modification_date']
                obj.reindexObject(idxs=['modified', ])
            if 'creation_date' in content:
                obj.creation_date = content['creation_date']
                obj.reindexObject(idxs=['created', ])
        if state is not None:
            api.content.transition(obj, to_state=state)
        if sub_contents is not None:
            create_ws_content(obj, sub_contents)


def library_spec(context):
    hr = {'type': 'ploneintranet.library.section',
          'title': 'Human Resources',
          'description': 'Information from the HR department',
          'contents': [
              {'type': 'ploneintranet.library.folder',
               'title': 'Leave policies',
               'description': 'Holidays and sick leave',
               'contents': [
                   {'type': 'Document',
                    'title': 'Holidays',
                    'desciption': 'Yearly holiday allowance'},
                   {'type': 'Document',
                    'title': 'Sick Leave',
                    'desciption': ("You're not feeling too well, "
                                   "here's what to do")},
                   {'type': 'Document',
                    'title': 'Pregnancy',
                    'desciption': 'Expecting a child?'},
               ]},
          ]}
    mixed_contents = []
    for i in range(3):
        mixed_contents.append({'type': 'ploneintranet.library.folder'})
    for i in range(5):
        mixed_contents.append({'type': 'Document'})
    mixedfolder = {'type': 'ploneintranet.library.folder',
                   'contents': mixed_contents}
    for i in range(3):
        # leave policies
        hr['contents'][0]['contents'].append(mixedfolder)
    for i in range(3):
        hr['contents'].append(mixedfolder)
    library = [hr]
    for i in range(4):
        library.append(
            {'type': 'ploneintranet.library.section',
             'contents': [mixedfolder] * 5}
        )
    return library


library_tags = (u'EU', u'Spain', u'UK', u'Belgium', u'confidential',
                u'onboarding',
                u'budget', u'policy', u'administration', u'press')


idcounter = 0


def create_library_content(parent,
                           spec,
                           force=False,
                           creator='alice_lindstrom',
                           bigsetup=False):
    if parent is None:
        # initial recursion
        portal = api.portal.get()
        parent = portal.library
        api.user.grant_roles(
            username=creator,
            roles=['Contributor', 'Reviewer', 'Editor'],
            obj=portal.library
        )
        try:
            api.content.transition(portal.library, 'publish')
        except api.exc.InvalidParameterError:
            # subsequent runs, already published
            pass
        # initial (automated testing) testcontent run: no children
        # second manual testcontent run: 1 child HR -> do big setup
        # subsequent manual testcontent runs: skip for speed
        already_setup = bool(len(portal.library.objectIds()) > 1)
        if already_setup and not force:
            log.info("library already setup. skipping for speed.")
            return

    # recursively called
    while spec:
        # avoiding side effects here cost me 4 hours!!
        item = copy.deepcopy(spec.pop(0))
        if 'title' not in item and not bigsetup:
            # skip lorem ipsum creation unless we're running bigsetup
            continue

        contents = item.pop('contents', None)
        if 'title' not in item:
            global idcounter
            idcounter += 1
            item['title'] = 'Lorem Ipsum %s' % idcounter
        if 'description' not in item:
            item['description'] = loremipsum.get_sentence()
        if item['type'] in ('Document',):
            raw_text = "\n\n".join(loremipsum.get_paragraphs(3))
            item['text'] = RichTextValue(raw=raw_text,
                                         mimeType='text/plain',
                                         outputMimeType='text/x-html-safe')

        obj = create_as(creator, container=parent, **item)
        if not item['type'].startswith('ploneintranet'):
            # only tag non-folderish content
            tags = random.sample(library_tags, random.choice(range(4)))
            tags.append(u'I ♥ UTF-8')
            wrapped = IDublinCore(obj)
            wrapped.subjects = tags
        api.content.transition(obj, 'publish')
        obj.reindexObject()  # or solr doesn't find it
        if contents:
            create_library_content(obj, contents, creator=creator,
                                   bigsetup=bigsetup)


def create_stream(context, stream, files_dir):
    hashtags = re.compile('#(\S+)')
    atmentions = re.compile('@(\S+)')
    contexts_cache = {}
    testfiles = {}
    abs_dir = os.path.join(os.path.dirname(__file__),
                           'profiles', 'testing', files_dir)
    for filename in os.listdir(abs_dir):
        with open(os.path.join(abs_dir, filename)) as fh:
            testfiles[filename.decode('utf-8')] = fh.read()
    like_tool = getUtility(INetworkTool)
    microblog = queryUtility(IMicroblogTool)
    microblog.clear()
    _orig_async = microblog.ASYNC
    microblog.ASYNC = False
    UTC = pytz.timezone('UTC')
    for status in stream:
        microblog_context = status['microblog_context']
        if microblog_context:
            if microblog_context not in contexts_cache:
                contexts_cache[microblog_context] = api.content.get(
                    path='/' + decode(microblog_context).lstrip('/')
                )
            m_context_obj = contexts_cache[microblog_context]
        offset_time = status['timestamp'] * 60
        _time = UTC.localize(
            datetime.utcfromtimestamp(time.time() - abs(offset_time)))
        status_obj = pi_api.microblog.statusupdate.create(
            text=status['text'],
            microblog_context=m_context_obj,
            mention_ids=atmentions.findall(status['text']),
            tags=hashtags.findall(status['text']),
            userid=status['user'],
            time=_time,
        )  # stored by pi_api
        # add attachments
        if 'attachment' in status:
            filename = status['attachment']['filename']
            data = testfiles[filename]
            status_obj.add_attachment(filename, data)
        # like some status-updates
        if 'likes' in status:
            for user_id in status['likes']:
                like_tool.like(
                    "update",
                    user_id=user_id,
                    item_id=str(status_obj.id),
                )
        for idx, reply in enumerate(status.get('replies', [])):
            pi_api.microblog.statusupdate.create(
                text=reply['text'],
                microblog_context=m_context_obj,
                userid=reply['author'],
                time=_time + timedelta(microseconds=idx),
                thread_id=status_obj.id,
            )

    microblog.ASYNC = _orig_async


def decode(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    return value


def create_as(userid, *args, **kwargs):
    """Call api.content.create as a different user
    """
    obj = None
    with api.env.adopt_user(username=userid):
        try:
            obj = api.content.create(*args, **kwargs)
        except:
            # we still need to know what happend
            raise
    return obj


def create_bookmarks():
    ''' Bookmark some applications
    '''
    pn = api.portal.get_tool('ploneintranet_network')
    portal = api.portal.get()
    workspaces = portal['workspaces']
    pn.bookmark(
        'content',
        workspaces['example-case'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        workspaces['shareholder-information'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        workspaces['example-case']['draft-proposal'].UID(),
        u'allan_neece'
    )
    manage_information = (
        workspaces['open-market-committee']['manage-information']
    )
    pn.bookmark(
        'content',
        manage_information['minutes'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        manage_information['minutes-overview'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        manage_information['budget-proposal'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['library']['human-resources']['leave-policies'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['apps']['bookmarks'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['profiles']['alice_lindstrom'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['profiles']['kurt_weissman'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['profiles']['pearlie_whitby'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['profiles']['silvio_depaoli'].UID(),
        u'allan_neece'
    )
    pn.bookmark(
        'content',
        portal['apps']['bookmarks'].UID(),
        u'fernando_poulter'
    )


def create_messages():
    """Generate some message traffic for testing ploneintranet.messaging.
    """
    inboxes = pi_api.messaging.get_inboxes()
    stamp = datetime(2016, 7, 1, 9, 23)
    for me in ('allan_neece', 'christian_stoney'):
        phrases = iter(PHRASES)
        for other in ('alice_lindstrom', 'guy_hackey', 'dollie_nocera'):
            inboxes.send_message(me, other, phrases.next(), stamp)
            stamp += timedelta(minutes=2)
            inboxes.send_message(other, me, phrases.next(), stamp)
            stamp += timedelta(minutes=1)
            inboxes.send_message(me, other, phrases.next(), stamp)
            stamp += timedelta(minutes=20)
            inboxes.send_message(me, other, phrases.next(), stamp)
            stamp += timedelta(minutes=2)
            inboxes.send_message(other, me, phrases.next(), stamp)
            stamp += timedelta(days=2)
            inboxes.send_message(other, me, phrases.next(), stamp)
            if other != 'guy_hackey':
                inboxes[me][other].mark_read()
    # another round to create a searchable inbox
    phrases = iter(PHRASES)
    me = 'guido_stevens'
    for other in ('francois_gast', 'esmeralda_claassen', 'jamie_jacko',
                  'fernando_poulter', 'jesse_shaik', 'jorge_primavera',
                  'alice_lindstrom', 'lance_stockstill', 'neil_wichmann'):
        inboxes.send_message(me, other, phrases.next(), stamp)
        stamp += timedelta(minutes=2)
        inboxes.send_message(other, me, phrases.next(), stamp)

PHRASES = [
    "Go and live with her, then! See if I care.",
    "Somehow we need to persuade him to part with a million dollars.",
    "Don't be scared. I just need you to come with me for a minute.",
    "I'm telling you - the guy was a complete stranger.",
    "This isn't just about you. It's about what's best for all of us.",
    "There's something I need to get off my chest.",
    "Don't upset your father, not now.",
    "I've been checking you out.",
    "You had time to call the police. Why didn't you?",
    "You're paying a small price compared with what she's going through.",
    "Why did you scream like that?",
    "What a thing to say - and on my birthday!",
    "I want to turn back the clock to before...",
    "Find some proof that she's betrayed you.",
    "You don't want to live in a society like this!",
    "Give me one good reason why I should wear a dress.",
    "What do you remember about your mother?",
    "I just want a nice, easy life. What's wrong with that?",
    "I'm ready to try again, if you are?",
]


def configure_news(*args):
    """Give alice_lindstrom full rights on the news app."""
    portal = api.portal.get()
    api.user.grant_roles(username='alice_lindstrom',
                         obj=portal.news,
                         roles=['Contributor', 'Editor', 'Reviewer'])
