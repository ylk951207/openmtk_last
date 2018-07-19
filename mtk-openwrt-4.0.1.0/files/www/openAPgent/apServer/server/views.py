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



'''
Device Info
'''
class DeviceInfoViewSet(viewsets.ModelViewSet):
    queryset = DeviceInfo.objects.all()
    serializer_class = DeviceInfoSerializer

'''
System Config
'''
class SystemConfigViewSet(viewsets.ViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer

    def list(self, request):
#    def list(self, request):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " list()" + "*" * 10)
        data = sal_system_config(SAL_METHOD_LIST, None)
        return Response(data, content_type='application/json')
        
    def create(self, request):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " create()" + "*" * 10)
        data = sal_system_config(SAL_METHOD_CREATE, request.data)
        return Response(data, content_type='application/json')

    def update(self, request):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " update()" + "*" * 10)
        data = sal_system_config(SAL_METHOD_UPDATE, request.data)
        return Response(data, content_type='application/json')


'''
Interfaces
'''
class InterfaceConfigViewSet(viewsets.ViewSet):
    def list(self, request):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " list()" + "*" * 10)
        data = sal_interface_config(SAL_METHOD_LIST, None, None)
        return Response(data, content_type='application/json')
        
    def retrieve(self, request, pk):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " retrieve()" + "*" * 10)
        token = request.path.split('/')
        ifname = token[-2]

        data = sal_interface_config(SAL_METHOD_RETRIEVE, None, ifname)
        return Response(data, content_type='application/json')

    def create(self, request, pk):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " create()" + "*" * 10)
        token = request.path.split('/')
        ifname = token[-2]
        
#        req_json = json.loads(request.body)
        data = sal_interface_config(SAL_METHOD_CREATE, request.data, ifname)
        return Response(data, content_type='application/json')
        
    def update(self, request, pk):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " update()" + "*" * 10)
        token = request.path.split('/')
        ifname = token[-2]
        
#        req_json = json.loads(request.body)
        data = sal_interface_config(SAL_METHOD_UPDATE, request.data, ifname)
        return Response(data, content_type='application/json')


'''
Generic Port Traffic
'''
class GenericIfStatsViewSet(viewsets.ViewSet):
    queryset = GenericIfStats.objects.all()
    serializer_class = GenericIfStatsSerializer

    def list(self, request):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " list()" + "*" * 10)
        data = sal_generic_ifstats(SAL_METHOD_LIST, None)
        return Response(data, content_type='application/json')

    def retrieve(self, request, pk):
        log_info(LOG_MODULE_APSERVER, "*" * 10 + " retrieve()" + "*" * 10)
        #Get ifname from url
        token = request.path.split('/')
        ifname = token[-2]

        data = sal_generic_ifstats(SAL_METHOD_RETRIEVE, ifname)
        if not data:
            raise Http404

        return Response(data, content_type='application/json')

