'''
This file was automatically generated by rmib_compiler.py.
 DO NOT EDIT.
'''


from python.provisioning import *
from swigc.sys_usage import *
from puci.system_config import *
from puci.interface import *
from puci.vlan import *
from puci.dhcp import *
from python.firmware import *
from python.docker_api import *


SAL_METHOD_LIST           = 1
SAL_METHOD_CREATE         = 2
SAL_METHOD_UPDATE         = 3
SAL_METHOD_RETRIEVE       = 4
SAL_METHOD_DETAIL_CREATE  = 5
SAL_METHOD_DETAIL_UPDATE  = 6
SAL_METHOD_PARTIAL_UPDATE = 7
SAL_METHOD_DESTROY        = 8



'''
 Define provisioning_done SAL function
'''
def sal_provisioning_done(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_CREATE:
    return py_provisioning_done_create(request)


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
 Define system_config SAL function
'''
def sal_system_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_system_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_system_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_system_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_system_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    return puci_system_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    return puci_system_config_detail_update(request, pk)


'''
 Define interface_config SAL function
'''
def sal_interface_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_interface_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_interface_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_interface_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_interface_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    return puci_interface_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    return puci_interface_config_detail_update(request, pk)


'''
 Define interface_v4addr_config SAL function
'''
def sal_interface_v4addr_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_interface_v4addr_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_interface_v4addr_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_interface_v4addr_config_update(request)


'''
 Define vlan_config SAL function
'''
def sal_vlan_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_vlan_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_vlan_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_vlan_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_vlan_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    return puci_vlan_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    return puci_vlan_config_detail_update(request, pk)


'''
 Define dhcp_common_config SAL function
'''
def sal_dhcp_common_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_dhcp_common_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_dhcp_common_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_dhcp_common_config_update(request)


'''
 Define dhcp_pool_config SAL function
'''
def sal_dhcp_pool_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_dhcp_pool_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_dhcp_pool_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_dhcp_pool_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_dhcp_pool_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    return puci_dhcp_pool_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    return puci_dhcp_pool_config_detail_update(request, pk)


'''
 Define dhcp_static_leases_config SAL function
'''
def sal_dhcp_static_leases_config(method, request, pk):
  # For Python-UCI APIs
  if method == SAL_METHOD_LIST:
    return puci_dhcp_static_leases_config_list()

  if method == SAL_METHOD_CREATE:
    return puci_dhcp_static_leases_config_create(request)

  if method == SAL_METHOD_UPDATE:
    return puci_dhcp_static_leases_config_update(request)

  if method == SAL_METHOD_RETRIEVE:
    return puci_dhcp_static_leases_config_retrieve(pk, 1)

  if method == SAL_METHOD_DETAIL_CREATE:
    return puci_dhcp_static_leases_config_detail_create(request, pk)

  if method == SAL_METHOD_DETAIL_UPDATE:
    return puci_dhcp_static_leases_config_detail_update(request, pk)


'''
 Define firmware_management SAL function
'''
def sal_firmware_management(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_firmware_management_list()

  if method == SAL_METHOD_CREATE:
    return py_firmware_management_create(request)


'''
 Define config_management SAL function
'''
def sal_config_management(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_LIST:
    return py_config_management_list()

  if method == SAL_METHOD_CREATE:
    return py_config_management_create(request)


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

  if method == SAL_METHOD_RETRIEVE:
    return py_docker_images_retrieve(pk, 1)

  if method == SAL_METHOD_CREATE:
    return py_docker_images_create(request)

  if method == SAL_METHOD_DETAIL_CREATE:
    return py_docker_images_detail_create(request, pk)

  if method == SAL_METHOD_DESTROY:
    return py_docker_images_destroy(request)

  if method == SAL_METHOD_DETAIL_DESTROY:
    return py_docker_images_detail_destroy(request, pk)


'''
 Define container_creation SAL function
'''
def sal_container_creation(method, request, pk):
  # For Python APIs
  if method == SAL_METHOD_CREATE:
    return py_container_creation_create(request)

  if method == SAL_METHOD_DETAIL_CREATE:
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
    return py_container_management_create(request)

  if method == SAL_METHOD_DETAIL_CREATE:
    return py_container_management_detail_create(request, pk)

