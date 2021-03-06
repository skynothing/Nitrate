# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db import models

from tcms.core.models import TCMSContentTypeBaseModel
from .managers import TCMSLogManager


# Create your models here.

class TCMSLogModel(TCMSContentTypeBaseModel):
    who = models.ForeignKey('auth.User', related_name='log_who')
    date = models.DateTimeField(auto_now_add=True)
    action = models.TextField()
    field = models.CharField(max_length=50, default='')
    original_value = models.TextField(default='')
    new_value = models.TextField(default='')

    objects = TCMSLogManager()

    class Meta:
        abstract = False
        db_table = u'tcms_logs'
        index_together = (('content_type', 'object_pk', 'site'),)

    def __str__(self):
        return self.action

    @classmethod
    def get_logs_for_model(cls, model_class, object_pk):
        ct = ContentType.objects.get_for_model(model_class)
        return cls.objects.filter(content_type=ct, object_pk=object_pk)
