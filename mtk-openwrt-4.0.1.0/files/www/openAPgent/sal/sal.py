'''
This file was automatically generated by rmib_compiler.py.
 DO NOT EDIT.
'''


from swigc.sys_usage import *
from python.system import *
from puci.system_config import *
from puci.interface import *
from puci.vlan import *
from puci.dhcp import *
from puci.snmp import *
from python.wireless import *
from puci.firewall import *
from python.firmware import *
from python.docker_api import *


import json
from common.misc import *
from common.message import *


SAL_METHOD_LIST           = 1
SAL_METHOD_CREATE         = 2
SAL_METHOD_UPDATE         = 3
SAL_METHOD_RETRIEVE       = 4
SAL_METHOD_DETAIL_CREATE  = 5
SAL_METHOD_DETAIL_UPDATE  = 6
SAL_METHOD_PARTIAL_UPDATE = 7
SAL_METHOD_DESTROY        = 8
SAL_METHOD_DETAIL_DESTROY = 9



'''
 Define system_usage SAL function
'''
def sal_system_usage(method, request, pk):
  # For SWIG C APIs
  if method == SAL_METHOD_LIST:
    return swigc_system_usage_list()

  if method == SAL_METHOD_RETRIEVE:
    return swigc_system_usage_retrieve(pk, 1)


'''
 Define system_info SAL function
'''
def sal_system_info(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_system_info_list()


'''
 Define system_time_info SAL function
'''
def sal_system_time_info(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_system_time_info_list()


'''
 Define interface_info SAL function
'''
def sal_interface_info(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_interface_info_list()

  if method == SAL_METHOD_RETRIEVE:
    return py_interface_info_retrieve(pk, 1)


'''
 Define interface_address_info SAL function
'''
def sal_interface_address_info(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_interface_address_info_list()

  if method == SAL_METHOD_RETRIEVE:
    return py_interface_address_info_retrieve(pk, 1)


'''
 Define wireless_info SAL function
'''
def sal_wireless_info(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_wireless_info_list()


'''
 Define wireless_station SAL function
'''
def sal_wireless_station(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_wireless_station_list()


'''
 Define wireless_search SAL function
'''
def sal_wireless_search(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_wireless_search_list()


'''
 Define dhcp_leases SAL function
'''
def sal_dhcp_leases(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_dhcp_leases_list()


'''
 Define provisioning_done SAL function
'''
def sal_provisioning_done(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_provisioning_done_create(request)


'''
 Define keepalive_check SAL function
'''
def sal_keepalive_check(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_keepalive_check_list()


'''
 Define system_config SAL function
'''
def sal_system_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_system_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_system_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_system_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_system_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_system_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_system_config_detail_update(request, pk)


'''
 Define interface_config SAL function
'''
def sal_interface_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_interface_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_interface_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_interface_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_interface_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_interface_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_interface_config_detail_update(request, pk)


'''
 Define interface_v4addr_config SAL function
'''
def sal_interface_v4addr_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_interface_v4addr_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_interface_v4addr_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_interface_v4addr_config_update(request)


'''
 Define vlan_config SAL function
'''
def sal_vlan_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_vlan_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_vlan_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_vlan_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_vlan_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_vlan_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_vlan_config_detail_update(request, pk)


'''
 Define dhcp_common_config SAL function
'''
def sal_dhcp_common_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_dhcp_common_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_common_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_common_config_update(request)


'''
 Define dhcp_pool_config SAL function
'''
def sal_dhcp_pool_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_dhcp_pool_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_pool_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_pool_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_dhcp_pool_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_pool_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_pool_config_detail_update(request, pk)


'''
 Define dhcp_static_leases_config SAL function
'''
def sal_dhcp_static_leases_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_dhcp_static_leases_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_static_leases_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_static_leases_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_dhcp_static_leases_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_static_leases_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_static_leases_config_detail_update(request, pk)

  if method == SAL_METHOD_DESTROY:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_static_leases_config_destroy(request)

  if method == SAL_METHOD_DETAIL_DESTROY:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_dhcp_static_leases_config_detail_destroy(request, pk)


'''
 Define snmp_config SAL function
'''
def sal_snmp_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_snmp_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_snmp_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_snmp_config_update(request)


'''
 Define wireless_config SAL function
'''
def sal_wireless_config(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_wireless_config_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_wireless_config_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_wireless_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return py_wireless_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_wireless_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_wireless_config_detail_update(request, pk)


'''
 Define port_forwarding SAL function
'''
def sal_port_forwarding(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_port_forwarding_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_port_forwarding_create(request)

  if method == SAL_METHOD_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_port_forwarding_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_port_forwarding_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_port_forwarding_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_port_forwarding_detail_update(request, pk)

  if method == SAL_METHOD_DESTROY:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_port_forwarding_destroy(request)

  if method == SAL_METHOD_DETAIL_DESTROY:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return puci_port_forwarding_detail_destroy(request, pk)


'''
 Define firmware_management SAL function
'''
def sal_firmware_management(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_firmware_management_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_firmware_management_create(request)


'''
 Define system_reboot SAL function
'''
def sal_system_reboot(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_system_reboot_create(request)


'''
 Define if_statistics SAL function
'''
def sal_if_statistics(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_if_statistics_list()

  if method == SAL_METHOD_RETRIEVE:
    return puci_if_statistics_retrieve(pk, 1)


'''
 Define docker_images SAL function
'''
def sal_docker_images(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_docker_images_list()

  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_docker_images_create(request)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_docker_images_detail_create(request, pk)


'''
 Define container_creation SAL function
'''
def sal_container_creation(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_container_creation_create(request)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_container_creation_detail_create(request, pk)


'''
 Define container_get SAL function
'''
def sal_container_get(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_container_get_list()

  if method == SAL_METHOD_RETRIEVE:
    return py_container_get_retrieve(pk, 1)


'''
 Define container_management SAL function
'''
def sal_container_management(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_container_management_create(request)

  if method == SAL_METHOD_DETAIL_CREATE:
    request = request_message_value_strip_all(request)
    log_info(LOG_MODULE_SAL, 'Request dump = ', json.dumps(request, indent=2))
    return py_container_management_detail_create(request, pk)

