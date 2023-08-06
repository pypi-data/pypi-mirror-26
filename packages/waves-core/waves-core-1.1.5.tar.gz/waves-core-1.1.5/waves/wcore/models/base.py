""" Django models bases classes """
from __future__ import unicode_literals

import re
import uuid

import inflection
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from waves.wcore.compat import RichTextField
from waves.wcore.settings import waves_settings as config

__all__ = ['TimeStamped', 'Ordered', 'ExportAbleMixin', 'Described', 'Slugged', 'ApiModel',
           'UrlMixin', 'WavesBaseModel']


class WavesBaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = "waves.wcore"


class TimeStamped(WavesBaseModel):
    """
    Time stamped 'able' models objects, add fields to inherited objects

    .. note::
        This class add also default ordering by -updated, -created (reverse order)

    """

    class Meta:
        abstract = True
        ordering = ['-updated', '-created']

    #: (auto_now_add): set when model object is created
    created = models.DateTimeField('Created on', auto_now_add=True, editable=False, help_text='Creation timestamp')
    #: (auto_now): set each time model object is saved in database
    updated = models.DateTimeField('Last Update', auto_now=True, editable=False, help_text='Last update timestamp')


class Ordered(WavesBaseModel):
    """ Order-able models objects,

    .. note::
        Default ordering field is set to 'order'
    """

    class Meta:
        abstract = True
        ordering = ['order']

    #: positive integer field (default to 0)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)


class Described(WavesBaseModel):
    """
    A model object which inherit from this class add two description fields to model objects

    """

    class Meta:
        abstract = True

    #: Text field to set up a complete description of model object, with HTML editor enabled
    description = RichTextField('Description', null=True, blank=True, help_text='Description (HTML)')
    #: text field for short version, no html
    short_description = models.TextField('Short Description', null=True, blank=True,
                                         help_text='Short description (Text)')


class Slugged(WavesBaseModel):
    """ Add a 'slug' field to models Objects, based on uuid.uuid4 field generator, this field is mainly used for models
    objects urls
    """

    class Meta:
        abstract = True

    #: UUID field is base on uuid4 generator.
    slug = models.UUIDField(default=uuid.uuid4, blank=True, unique=True, editable=False)


class ApiModel(WavesBaseModel):
    """
    An API-able model object need a 'api_name', in order to setup dedicated url for this model object
    """

    class Meta:
        abstract = True

    field_api_name = 'name'
    #: A char field, must be unique for a model instance
    api_name = models.CharField(max_length=100, null=True, blank=True,
                                help_text='Api short code, must be unique, leave blank for automatic setup')

    @property
    def base_api_name(self):
        last_pos = self.api_name.rfind('_')
        if last_pos != -1 and self.api_name[last_pos + 1:].isdigit():
            print 'base_api_name 1', self.api_name[:last_pos+1]
            return self.api_name[:last_pos+1]
        else:
            print "simple api_name ", self.api_name
            return self.api_name

    def duplicate_api_name(self, api_name):
        """ Check is another entity is set with same api_name
        :param api_name:
        """
        return self.__class__.objects.filter(api_name=api_name).exclude(pk=self.pk)

    def create_api_name(self):
        """
        Construct a new wapi:api_v2 name issued from field_api_name
        :return:
        """
        return inflection.underscore(re.sub(r'[^\w]+', '_', getattr(self, self.field_api_name))).lower()

    def clean(self):
        try:
            if self.duplicate_api_name(self.api_name).count() > 0:
                raise ValidationError({'api_name': 'Value must be unique'})
        except MultipleObjectsReturned:
            raise ValidationError({'api_name': "Value is not unique"})
        except ObjectDoesNotExist:
            pass


class UrlMixin(object):
    """ Url Mixin allow easy generation or absolute url related to any model object

    .. note::
       Sub-classes must define a get_absolute_url() method > See
       `Django get_absolute_url <https://docs.djangoproject.com/en/1.9/ref/models/instances/#get-absolute-url>`_
    """

    @property
    def link(self):
        """ short cut to :func:`get_url()`
        :return: current absolute uri for Job
        """
        return "%s%s" % (config.HOST, self.get_absolute_url())

    def get_url(self):
        """ Calculate and return absolute 'front-office' url for a model object
        :return: unicode the absolute url
        """
        return self.get_absolute_url()

    def get_absolute_url(self):
        raise NotImplementedError


class ExportError(Exception):
    """ Export 'Error'"""
    pass


class ExportAbleMixin(object):
    """ Some models object may be 'exportable' in order to be imported elsewhere in another WAVES app.
    Based on Django serializer, because we don't want to select fields to export
    """

    def serializer(self, context=None):
        """ Each sub class must implement this method to initialize its Serializer"""
        raise NotImplementedError('Sub classes must implements this method')

    def serialize(self):
        """ Import model object serializer, serialize and write data to disk """
        from os.path import join
        import json
        file_path = join(config.DATA_ROOT, self.export_file_name)
        with open(file_path, 'w') as fp:
            try:
                serializer = self.serializer()
                data = serializer.to_representation(self)
                fp.write(json.dumps(data, indent=2))
                return file_path
            except Exception as e:
                raise ExportError('Error dumping model %s [%s]' % (self, e))

    @property
    def export_file_name(self):
        """ Create export file name, based on concrete class name"""
        return '%s_%s.json' % (self.__class__.__name__.lower(), str(self.pk))
