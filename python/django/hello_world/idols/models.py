# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Idol(models.Model):
    name = models.CharField(max_length=200)
    birthday = models.DateField()
    def __unicode__(self):
        return self.name


class Video(models.Model):
    subject     = models.CharField(max_length=200, default='undefined')
    link        = models.CharField(max_length=200)
    pub_date    = models.DateField()
    idol        = models.ForeignKey(Idol, on_delete=models.CASCADE, default=1)
    def __unicode__(self):
        return self.subject
    