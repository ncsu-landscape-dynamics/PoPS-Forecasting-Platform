import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse

from users.models import CustomUser

class Topic(models.Model):
    name = models.CharField(verbose_name = _("topic name"), max_length = 150)
    sort_order = models.IntegerField(verbose_name = _("sort order"), default = 0)
    slug = models.SlugField(verbose_name = _('slug'), max_length = 150)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("faq_topic_detail", args = (self.slug,))
    
class Question(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE,    _('Active')),
        (INACTIVE,  _('Inactive')),
        (HEADER,    _('Group Header')),
    )

    question_text = models.CharField(verbose_name = _('question'), max_length = 150)
    slug = models.SlugField(verbose_name = _('slug'), max_length = 150)
    answer = models.TextField(verbose_name = _('answer'))
    topic = models.ForeignKey(Topic, on_delete = models.PROTECT)
    status = models.IntegerField(verbose_name = _('status'), choices = STATUS_CHOICES, default = INACTIVE)
    created_on = models.DateTimeField(verbose_name = _('date created'), default = datetime.datetime.now(), editable = False)
    updated_on = models.DateTimeField(verbose_name = _('date updated'), default = datetime.datetime.now(), editable = False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, related_name = "+", on_delete = models.SET_NULL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('updated by'), editable = False,
        null = True, related_name = "+", on_delete = models.SET_NULL)
    helpful_yes = models.IntegerField(verbose_name = _('helpful'), default = 0)
    helpful_no = models.IntegerField(verbose_name = _('not helpful'), default = 0)
    sort_order = models.IntegerField(verbose_name = _('sort order'), default = 0)

    class Meta:
        verbose_name = _("Frequently asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order', 'helpful_yes']

    def get_absolute_url(self):
        return reverse("faq_question_detail", [self.topic.slug, self.slug])
    
    def is_header(self):
        return self.status == Question.HEADER

    def is_active(self):
        return self.status == Question.ACTIVE
