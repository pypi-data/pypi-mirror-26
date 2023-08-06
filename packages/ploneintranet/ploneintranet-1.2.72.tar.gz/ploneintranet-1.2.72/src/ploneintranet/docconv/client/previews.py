# -*- coding: utf-8 -*-
from collective.documentviewer import storage
from collective.documentviewer.convert import Converter as DVConverter
from collective.documentviewer.convert import DocSplitSubProcess
from collective.documentviewer.convert import DUMP_FILENAME
from collective.documentviewer.convert import TEXT_REL_PATHNAME
from collective.documentviewer.interfaces import IFileWrapper
from collective.documentviewer.interfaces import IOCRLanguage
from collective.documentviewer.settings import GlobalSettings
from collective.documentviewer.settings import Settings
from collective.documentviewer.utils import allowedDocumentType
from collective.documentviewer.utils import getPortal
from datetime import datetime
from logging import getLogger
from plone import api
from ploneintranet.docconv.client.html_converter import generate_pdf
from Products.MimetypesRegistry.common import MimeTypeException
from urllib import urlencode
from zope.annotation import IAnnotations
from zope.site.hooks import getSite

import os
import shutil


log = getLogger(__name__)

PREVIEW_URL = '++theme++ploneintranet.theme/generated/media/logos/plone-intranet-square.svg'  # noqa


class PIDocSplitSubProcess(DocSplitSubProcess):
    """
    idea of how to handle this shamelessly
    stolen from ploneformgen's gpg calls
    """

    if os.name == 'nt':
        bin_name = 'docsplit.exe'
    else:
        bin_name = 'docsplit'

    def dump_images(self, filepath, output_dir, sizes, format, lang='eng'):
        # docsplit images pdf.pdf --size 700x,300x,50x
        # --format gif --output
        limit = api.portal.get_registry_record(
            'ploneintranet.docconv.num_previews',
            default=20)
        pages = self.get_num_pages(filepath)
        if pages < limit:
            limit = pages
        cmd = [
            self.binary, "images", filepath,
            '--language', lang,
            '--size', ','.join([str(s[1]) + 'x' for s in sizes]),
            '--format', format,
            '--rolling',
            '--output', output_dir,
            '--pages', '1-%s' % limit]
        if lang != 'eng':
            # cf https://github.com/documentcloud/docsplit/issues/72
            # the cleaning functions are only suited for english
            cmd.append('--no-clean')

        self._run_command(cmd)

        # now, move images to correctly named folders
        for name, size in sizes:
            dest = os.path.join(output_dir, name)
            if os.path.exists(dest):
                shutil.rmtree(dest)

            source = os.path.join(output_dir, '%ix' % size)
            shutil.move(source, dest)

try:
    docsplit = PIDocSplitSubProcess()
except IOError:
    log.exception("No docsplit installed. pi.preview generation will not work")
    docsplit = None


class Converter(DVConverter):
    """ This class overrides the Converter class of collective.documentviewer
        which forces its own layout on converted content objects. We need to
        use our own layout, so this is deactivated.
    """

    def handle_layout(self):
        """
        Deactivate the layout setting part of documentviewer as we want our own
        """
        pass

    def run_conversion(self):
        """ override to run our own docsplit process """
        context = self.context
        gsettings = self.gsettings
        fw = IFileWrapper(context)
        filename = fw.filename
        language = IOCRLanguage(context).getLanguage()
        args = dict(sizes=(('large', gsettings.large_size),
                           ('normal', gsettings.normal_size),
                           ('small', gsettings.thumb_size)),
                    enable_indexation=self.isIndexationEnabled(),
                    ocr=gsettings.ocr,
                    detect_text=gsettings.detect_text,
                    format=gsettings.pdf_image_format,
                    converttopdf=self.doc_type.requires_conversion,
                    language=language,
                    filename=filename)
        if self.blob_filepath is None:
            args['filedata'] = str(fw.file.data)
        else:
            args['inputfilepath'] = self.blob_filepath

        return docsplit.convert(self.storage_dir, **args)


def _backward_map(scale):
    """ Provide a mapping from plone scale names to collective.documentviewer
    scale names for convenience. This assures that code can use both naming
    conventions.

    :param scale: The name of a scale
    :type scale: A string
    :return: The corresponding name of the scale as understood by c.dv
    :rtype: string
    """
    if scale == 'thumb':
        return 'small'
    elif scale == 'preview':
        return 'normal'
    elif scale == 'large':
        return 'large'
    if scale not in ('large', 'normal', 'small'):
        scale = 'large'  # default to a size that will never be pixeled

    return scale


def _get_dv_data(obj):
    """ Access the collective.documentviewer settings of an object and
    return metadata that can be used to retrieve or access a preview
    image.

    :param obj: The Plone content object that has a preview
    :type obj: A Plone content object
    :return: Metadata consisting of canonical_url, number of pages and
    resource urls to preview images and thumbnails.
    :rtype: mapping
    """
    site = getSite()
    global_settings = GlobalSettings(site)
    settings = Settings(obj)
    portal_url = site.portal_url()

    try:
        canonical_url = obj.absolute_url()
    except AttributeError:
        canonical_url = ''  # XXX construct a url to an attachment

    if not hasattr(obj, 'UID') or not settings.successfully_converted:
        # Can't have previews on objects without a UID. Return a
        # minimal datastructure
        return {
            'canonical_url': canonical_url + '/view',
            'pages': settings.num_pages,
            'resources': {
                'page': {
                    'image': fallback_image_url(obj),
                    'text': ''
                },
                'pdf': canonical_url,
                'thumbnail': fallback_image_url(obj),
            }
        }

    resource_url = global_settings.override_base_resource_url
    rel_url = storage.getResourceRelURL(gsettings=global_settings,
                                        settings=settings)
    if resource_url:
        dvpdffiles = '%s/%s' % (resource_url.rstrip('/'),
                                rel_url)
    else:
        dvpdffiles = '%s/%s' % (portal_url, rel_url)
    dump_path = DUMP_FILENAME.rsplit('.', 1)[0]

    image_format = settings.pdf_image_format or \
        global_settings.pdf_image_format

    return {
        'canonical_url': canonical_url + '/view',
        'pages': settings.num_pages,
        'resources': {
            'page': {
                'image': '%s/{size}/%s_{page}.%s' % (
                    dvpdffiles, dump_path,
                    image_format),
                'text': '%s/%s/%s_{page}.txt' % (
                    dvpdffiles, TEXT_REL_PATHNAME, dump_path)
            },
            'pdf': canonical_url,
            'thumbnail': '%s/small/%s_1.%s' % (
                dvpdffiles, dump_path,
                image_format),
        }
    }


def get(obj, scale='normal'):
    """Get the preview images for the given object

    If there are currently no previews, an empty list will be returned

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: The preview images
    :rtype: list
    """
    previews = []
    settings = Settings(obj)
    if settings.blob_files and settings.num_pages:
        ext = settings.pdf_image_format
        scale = _backward_map(scale)
        for i in range(len(settings.blob_files)):
            preview = '%s/dump_%s.%s' % (scale, str(i + 1), ext)
            if settings.blob_files.get(preview, False):
                previews.append(settings.blob_files[preview])
    return previews


def is_allowed_document_type(obj):
    """ Check if object can actually be converted

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: True if object can be converted
    :rtype: boolean
    """
    site = getPortal(obj)
    gsettings = GlobalSettings(site)
    try:
        return allowedDocumentType(obj, gsettings.auto_layout_file_types)
    except MimeTypeException as e:
        log.warning(
            'Mimetype issue for %r: %s',
            obj,
            e,
        )
        return False


def converting(obj):
    """ Check if object is currently being converted

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: True if converting, False if no longer converting
    :rtype: boolean
    """
    settings = Settings(obj)
    return settings.converting


def successfully_converted(obj):
    """ Check if object could be converted

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: True if successfully converted, False if conversion failed
    :rtype: boolean
    """
    settings = Settings(obj)
    return settings.successfully_converted


def has_previews(obj):
    """Test if the object has generated previews.

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: True if there are previews. False otherwise.
    :rtype: boolean
    """
    if get(obj):
        return True
    return False


def get_preview_urls(obj, scale='normal', with_timestamp=False):
    """Convenience method to get URLs of image previews as these are most
    frequently used

    :param obj: The Plone content object to get preview URLs for
    :type obj: A Plone content object
    :param with_timestamp: If True add a timestamp to the URLs
    :type with_timestamp: bool
    :param scale: The Plone image scale to get preview images at
    :type scale: str
    :return: List of preview image absolute URLs
    :rtype: list
    """
    dv_data = _get_dv_data(obj)
    scale = _backward_map(scale)
    settings = Settings(obj)
    if not settings or settings.blob_files is None:
        return [fallback_image_url(obj)]
    previews = []
    ext = settings.pdf_image_format
    for i in range(len(settings.blob_files)):
        preview = '%s/dump_%s.%s' % (scale, str(i + 1), ext)
        if settings.blob_files.get(preview, False):
            previews.append(settings.blob_files[preview])

    number_of_previews = dv_data['pages']

    # If there aren't any previews, return the placeholder url
    if number_of_previews < 1:
        return [fallback_image_url(obj)]
    urls = [
        dv_data['resources']['page']['image'].format(size=scale, page=page)
        for page in range(1, len(previews) + 1)
    ]
    if with_timestamp:
        try:
            timestamp = Settings(obj).last_updated
        except:
            log.exception('Cannot get timestamp from %r', obj)
            timestamp = datetime.now().isoformat()
        qs = '?%s' % urlencode({'t': timestamp})
        urls = [(url + qs) for url in urls]
    return urls


def fallback_image(obj):
    """Return a fallback image for use if there are no previews.

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: An image object
    :rtype: ZODB.blob.Blob
    """
    return api.portal.get().restrictedTraverse(PREVIEW_URL)


def fallback_image_url(obj):
    """Return a fallback image URL for use if there are no previews.

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: An image object url
    :rtype: string
    """
    return '{0}/{1}'.format(api.portal.get().absolute_url(), PREVIEW_URL)


def get_thumbnail(obj):
    """Get the thumnail preview image for the given object

    :param obj: The Plone object to get previews for
    :type obj: A Plone content object
    :return: The preview thumbnail
    :rtype: ImageScaling
    """
    previews = get(obj, scale='small')
    if len(previews) < 1:
        return fallback_image(obj)
    return previews[0]


def _resource_url_by_uid(uid):
    """ assuming we know we have a thumbnail, we can generate the path
        using the uid only.
        This code is mimicking c.docmentviewer.storage.getResourceRelURL:38
        which is building the same from an object instead only an uid.
    """
    if not uid:
        return PREVIEW_URL
    base = '@@dvpdffiles/'
    return '%s%s/%s/%s' % (base, uid[0], uid[1], uid)


def get_thumbnail_url_by_uid(uid, relative=False):
    site = getSite()
    portal_url = site.portal_url()
    global_settings = GlobalSettings(site)
    resource_url = global_settings.override_base_resource_url
    rel_url = _resource_url_by_uid(uid)
    if resource_url:
        dvpdffiles = '%s/%s' % (resource_url.rstrip('/'),
                                rel_url)
    else:
        dvpdffiles = '%s/%s' % (portal_url, rel_url)
    dump_path = DUMP_FILENAME.rsplit('.', 1)[0]
    image_format = global_settings.pdf_image_format
    thumbnail_url = '%s/small/%s_1.%s' % (
                    dvpdffiles, dump_path,
                    image_format)
    if relative:
        portal = api.portal.get()
        thumbnail_url = thumbnail_url.replace(portal.absolute_url(),
                                              portal.absolute_url(1))
    return thumbnail_url


def get_thumbnail_url(obj, relative=False):
    """Convenience method to get the absolute URL of thumbnail image

    :param obj: The Plone content object to get preview URLs for
    :type obj: A Plone content object
    :return: The absolute URL to the thumbnail image
    :rtype: str
    """
    dv_data = _get_dv_data(obj)
    thumbnail_url = dv_data['resources']['thumbnail']
    if relative:
        portal = api.portal.get()
        thumbnail_url = thumbnail_url.replace(portal.absolute_url(),
                                              portal.absolute_url(1))
    return thumbnail_url


def has_pdf(obj):
    """ NOT IMPLEMENTED. Once we do pdf generation for text content, this will work

    :param obj: The Plone content object to get preview URLs for
    :type obj: A Plone content object
    :return: True if there is a pdf available
    :rtype: boolean
    """
    return False


def get_pdf(obj):
    """ NOT IMPLEMENTED. Once we do pdf generation for text content, this will work

    :param obj: The Plone content object to get preview URLs for
    :type obj: A Plone content object
    :return: The generated pdf preview of the content item
    :rtype: Blob
    """
    return None


def generate_previews(obj, event=None):
    """ Generate the previews for a content type. We need our own subscriber as
    c.dv insists on checking for its custom layout. Also we want our own async
    mechanism, it is using this method.

    :param obj: The Plone content object to get preview URLs for
    :type obj: A Plone content object
    :return: Does not return anything.
    :rtype: None
    """
    site = getPortal(obj)
    gsettings = GlobalSettings(site)
    html_types = api.portal.get_registry_record(
        'ploneintranet.docconv.html_types',
        default=[],
    )

    if obj.portal_type in html_types:
        generate_pdf(obj, event=event)

    if not allowedDocumentType(obj, gsettings.auto_layout_file_types):
        log.info('Object type is not in available file types for conversion.')
        return

    if gsettings.auto_convert:
        converter = Converter(obj)
        if not converter.can_convert:
            return
        converter()


def purge_previews(obj):
    '''
    Purge the previews from obj

    :param obj: The Plone content object for which we want to purge
                the previews
    :type obj: A Plone content object
    :return: Does not return anything.
    :rtype: None
    '''
    IAnnotations(obj).pop('collective.documentviewer', {})
    Settings(obj)
