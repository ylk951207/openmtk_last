# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from common.env import *
from common.misc import *
from sal.puci.interface import *
from apServer.server.custom_views import *
from apServer.server.models import *
from apServer.server.serializers import *

class hardwareInfoView(APIView):
	def get(self, pk):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "hardwareInfoView list()" + "*" * 10)
		data = hardware_info_list()
		return Response(data, content_type='application/json')


class InterfaceV4AddrConfigView(APIView):
	def get(self, pk, ifname):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "InterfaceV4AddrConfigView list()" + "*" * 10)
		log_info(LOG_MODULE_APSERVER, "ifname: " + str(ifname))
		data = puci_interface_v4addr_config_list(str(ifname))
		return Response(data, content_type='application/json')

	def post(self, request, ifname, format=None):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "InterfaceV4AddrConfigView create()" +  "*" * 10)
		log_info(LOG_MODULE_APSERVER, "ifname: " + str(ifname))
		data = puci_interface_v4addr_config_create(request.data, str(ifname))
		return Response(data, content_type='application/json')

	def put(self, request, ifname, format=None):
		log_info(LOG_MODULE_APSERVER, "*" * 10 + "InterfaceV4AddrConfigView update()" + "*" * 10)
		log_info(LOG_MODULE_APSERVER, "ifname: " + str(ifname))
		data = puci_interface_v4addr_config_update(request.data, str(ifname))
		return Response(data, content_type='application/json')
