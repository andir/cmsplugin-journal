import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

class Category(models.Model):
    title           = models.CharField(_('Title'), max_length=255)
    slug            = models.SlugField(_('Slug'), unique=True,
                        help_text=_('A slug is a short name which uniquely identifies the category'))
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('title',)

    def __unicode__(self):
        return self.title
    
class PublishedEntryManager(models.Manager):
    """
        Filters out all unpublished and items with a publication date in the future
    """
    def get_query_set(self):
        return super(PublishedEntryManager, self).get_query_set() \
                    .filter(is_published=True) \
                    .filter(pub_date__lte=datetime.datetime.now())
    
class Entry(models.Model):
    """
    Entry
    """
    
    title           = models.CharField(_('Title'), max_length=255)
    slug            = models.SlugField(_('Slug'), unique_for_date='pub_date', 
                        help_text=_('A slug is a short name which uniquely identifies the news item for this day'))
    excerpt         = models.TextField(_('Excerpt'), blank=True)
    content         = models.TextField(_('Content'), blank=True)
    image           = models.ImageField(_('Image'), upload_to="journal_images", blank=True, null=True)
    alignment       = models.CharField(_("Alignment"), help_text=_("Alignment of the image"), max_length=5, choices=((_("Left"), "left"), (_("Right"), "right")), blank=True, null=True)
    
    is_published    = models.BooleanField(_('Published'), default=True)
    pub_date        = models.DateTimeField(_('Publication date'), default=datetime.datetime.now())
    
    created         = models.DateTimeField(auto_now_add=True, editable=False)
    updated         = models.DateTimeField(auto_now=True, editable=False)

    category        = models.ForeignKey(Category, null=True)
    
    published = PublishedEntryManager()
    objects = models.Manager()
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ('-pub_date', )
    
    def __unicode__(self):
        return self.title

    def get_relative_url_archive_index(self):
        return '%s/%s/' % (self.pub_date.strftime('%Y/%m/%d'), self.slug)
    
    def get_relative_url_archive_year(self):
        return '%s/%s/' % (self.pub_date.strftime('%m/%d'), self.slug)
    
    def get_relative_url_archive_month(self):
        return '%s/%s/' % (self.pub_date.strftime('%d'), self.slug)
    
    def get_relative_url_archive_day(self):
        return '%s/' % self.slug

    def get_relative_url(self):
        return self.get_relative_url_archive_index()
    
class LatestEntryPlugin(CMSPlugin):
    """
        Model for the settings when using the latest entries cms plugin
    """
    title = models.CharField(_('Title'), max_length=255)
    limit = models.PositiveIntegerField(_('Number of entries to show'), 
                    help_text=_('Limits the number of entries that will be displayed'))
    category = models.ManyToManyField(Category, blank=True, null=True, help_text=_("Leave this field blank to match all categories"))

