from wapi.interface import *
from wapi.system import *

'''
Define SAL Method
'''
SAL_METHOD_LIST=1
SAL_METHOD_RETRIEVE=2
SAL_METHOD_CREATE=3
SAL_METHOD_UPDATE=4
SAL_METHOD_PARTIAL_UPDATE=5
SAL_METHOD_DELETE=6


def sal_system_config(method, req):
    if method == SAL_METHOD_LIST:
        return system_config_list()
    if method == SAL_METHOD_CREATE:
        return system_config_create(req)
    if method == SAL_METHOD_UPDATE:
        return system_config_update(req)
    else:
        return None

def sal_interface_config(method, req, ifname):
    if method == SAL_METHOD_LIST:
        return interface_config_list()
    elif method == SAL_METHOD_RETRIEVE:
        if not ifname: return None
        return interface_config_retrieve(ifname, 1)
    elif method == SAL_METHOD_CREATE:
        return interface_config_create(req, ifname)
    elif method == SAL_METHOD_UPDATE:
        return interface_config_update(req, ifname)
    else:
        return None

def sal_generic_ifstats(method, ifname):
    if method == SAL_METHOD_LIST:
        return generic_ifstats_list()
    elif method == SAL_METHOD_RETRIEVE:
        if not ifname: return None
        return generic_ifstats_retrieve(ifname)
    else:
        return None

