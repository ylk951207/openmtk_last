# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import subprocess
import shlex
import fileinput
import json
from django.http import Http404
from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apServer.server.models import *
from apServer.server.serializers import *
from common.log import *
from common.env import *
from sal.sal import *
from apServer.server.custom_views import *


'''
Device Info
'''
class DeviceInfoViewSet(viewsets.ModelViewSet):
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceInfoSerializer

