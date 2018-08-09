import fileinput

from puci import *
from common.log import *
from common.env import *

UCI_DHCP_COMMON_CONFIG = "dhcp_common"
UCI_DHCP_INTERFACE_POOL_CONFIG = "dhcp_interface_pool"
UCI_DHCP_INTERFACE_V6POOL_CONFIG = "dhcp_interface_v6pool"
UCI_DHCP_STATIC_LEASE_CONFIG = "dhcp_static_lease"

