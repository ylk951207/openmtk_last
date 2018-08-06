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


class InterfaceV4AddrConfigView(APIView):
	def get(self, pk, ifname):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "InterfaceV4AddrConfigView list()" + "*" * 10)
		log_info(LOG_MODULE_APSERVER, "ifname: " + str(ifname))
		data = sal_interface_v4addr_config(SAL_METHOD_LIST, None, str(ifname))
		return Response(data, content_type='application/json')

	def post(self, request, ifname, format=None):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "InterfaceV4AddrConfigView create()" +  "*" * 10)
		log_info(LOG_MODULE_APSERVER, "ifname: " + str(ifname))
		data = sal_interface_v4addr_config(SAL_METHOD_CREATE, request.data, str(ifname))
		return Response(data, content_type='application/json')

	def put(self, request, ifname, format=None):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "InterfaceV4AddrConfigView update()" + "*" * 10)
		log_info(LOG_MODULE_APSERVER, "ifname: " + str(ifname))
		data = sal_interface_v4addr_config(SAL_METHOD_UPDATE, request.data, str(ifname))
		return Response(data, content_type='application/json')
