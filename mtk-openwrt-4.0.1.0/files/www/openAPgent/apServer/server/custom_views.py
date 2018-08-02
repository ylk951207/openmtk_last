'''
This file was automatically generated by rmib_compiler.py.
DO NOT EDIT.
'''


import json
from rest_framework import status, viewsets
from rest_framework.response import Response
from sal.sal import *
from common.log import *



'''
 Define Class SysetmConfig
'''
class SysetmConfigViewSet(viewsets.ViewSet):
  def list(self, request):
    log_info(LOG_MODULE_APSERVER, "*** SysetmConfig list() ***")
    data = sal_system_config(SAL_METHOD_LIST, request.data, None)
    return Response(data, content_type='application/json')

  def create(self, request):
    log_info(LOG_MODULE_APSERVER, "*** SysetmConfig create() ***")
    data = sal_system_config(SAL_METHOD_CREATE, request.data, None)
    return Response(data, content_type='application/json')

  def update(self, request):
    log_info(LOG_MODULE_APSERVER, "*** SysetmConfig update() ***")
    data = sal_system_config(SAL_METHOD_UPDATE, request.data, None)
    return Response(data, content_type='application/json')

  def retrieve(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** SysetmConfig retrieve(), pk = " + pk + " ***")
    data = sal_system_config(SAL_METHOD_RETRIEVE, request.data, pk)
    return Response(data, content_type='application/json')

  def detail_create(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** SysetmConfig detail_create(), pk = " + pk + " ***")
    data = sal_system_config(SAL_METHOD_DETAIL_CREATE, request.data, pk)
    return Response(data, content_type='application/json')

  def detail_update(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** SysetmConfig detail_update(), pk = " + pk + " ***")
    data = sal_system_config(SAL_METHOD_DETAIL_UPDATE, request.data, pk)
    return Response(data, content_type='application/json')



'''
 Define Class InterfaceConfig
'''
class InterfaceConfigViewSet(viewsets.ViewSet):
  def list(self, request):
    log_info(LOG_MODULE_APSERVER, "*** InterfaceConfig list() ***")
    data = sal_interface_config(SAL_METHOD_LIST, request.data, None)
    return Response(data, content_type='application/json')

  def create(self, request):
    log_info(LOG_MODULE_APSERVER, "*** InterfaceConfig create() ***")
    data = sal_interface_config(SAL_METHOD_CREATE, request.data, None)
    return Response(data, content_type='application/json')

  def update(self, request):
    log_info(LOG_MODULE_APSERVER, "*** InterfaceConfig update() ***")
    data = sal_interface_config(SAL_METHOD_UPDATE, request.data, None)
    return Response(data, content_type='application/json')

  def retrieve(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** InterfaceConfig retrieve(), pk = " + pk + " ***")
    data = sal_interface_config(SAL_METHOD_RETRIEVE, request.data, pk)
    return Response(data, content_type='application/json')

  def detail_create(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** InterfaceConfig detail_create(), pk = " + pk + " ***")
    data = sal_interface_config(SAL_METHOD_DETAIL_CREATE, request.data, pk)
    return Response(data, content_type='application/json')

  def detail_update(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** InterfaceConfig detail_update(), pk = " + pk + " ***")
    data = sal_interface_config(SAL_METHOD_DETAIL_UPDATE, request.data, pk)
    return Response(data, content_type='application/json')



'''
 Define Class VlanConfig
'''
class VlanConfigViewSet(viewsets.ViewSet):
  def list(self, request):
    log_info(LOG_MODULE_APSERVER, "*** VlanConfig list() ***")
    data = sal_vlan_config(SAL_METHOD_LIST, request.data, None)
    return Response(data, content_type='application/json')

  def create(self, request):
    log_info(LOG_MODULE_APSERVER, "*** VlanConfig create() ***")
    data = sal_vlan_config(SAL_METHOD_CREATE, request.data, None)
    return Response(data, content_type='application/json')

  def update(self, request):
    log_info(LOG_MODULE_APSERVER, "*** VlanConfig update() ***")
    data = sal_vlan_config(SAL_METHOD_UPDATE, request.data, None)
    return Response(data, content_type='application/json')

  def retrieve(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** VlanConfig retrieve(), pk = " + pk + " ***")
    data = sal_vlan_config(SAL_METHOD_RETRIEVE, request.data, pk)
    return Response(data, content_type='application/json')

  def detail_create(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** VlanConfig detail_create(), pk = " + pk + " ***")
    data = sal_vlan_config(SAL_METHOD_DETAIL_CREATE, request.data, pk)
    return Response(data, content_type='application/json')

  def detail_update(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** VlanConfig detail_update(), pk = " + pk + " ***")
    data = sal_vlan_config(SAL_METHOD_DETAIL_UPDATE, request.data, pk)
    return Response(data, content_type='application/json')



'''
 Define Class IfStatistics
'''
class IfStatisticsViewSet(viewsets.ViewSet):
  def list(self, request):
    log_info(LOG_MODULE_APSERVER, "*** IfStatistics list() ***")
    data = sal_if_statistics(SAL_METHOD_LIST, request.data, None)
    return Response(data, content_type='application/json')

  def retrieve(self, request, pk):
    log_info(LOG_MODULE_APSERVER, "*** IfStatistics retrieve(), pk = " + pk + " ***")
    data = sal_if_statistics(SAL_METHOD_RETRIEVE, request.data, pk)
    return Response(data, content_type='application/json')

