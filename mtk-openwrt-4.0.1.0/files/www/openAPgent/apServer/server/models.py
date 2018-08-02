# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from common.env import *


class DeviceInfo(models.Model):
    device_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    vendor_id = models.IntegerField(default=-1)
    vendor_name = models.CharField(max_length=100, default='')
    serial_num = models.CharField(max_length=100, default=-1)
    device_type = models.IntegerField(default=-1)
    model_num = models.IntegerField(default=-1)
    ip_addr = models.CharField(max_length=100, default='')
    mac_addr = models.CharField(max_length=100, default='')
    user_id = models.CharField(max_length=100, default=-1)
    user_passwd = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=-1)
    map_x = models.CharField(max_length=100, default='')
    map_y = models.CharField(max_length=100, default='')
    counterfeit = models.BooleanField()

    def __unicode__(self):
        return self.name

