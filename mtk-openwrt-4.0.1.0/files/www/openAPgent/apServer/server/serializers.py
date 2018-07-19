from rest_framework import serializers
from apServer.server.models import *

class DeviceInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = ('device_id', 
                  'name', 
                  'vendor_id', 
                  'vendor_name', 
                  'serial_num', 
                  'device_type', 
                  'model_num',
                  'ip_addr', 
                  'mac_addr', 
                  'user_id', 
                  'user_passwd', 
                  'status', 
                  'map_x', 
                  'map_y', 
                  'counterfeit')


class SystemConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SystemConfig
        fields = ('enable_ntp_client', 
                  'provide_ntp_server', 
                  'ntp_server_candidates', 
                  'logging_buffer_size',
                  'logging_server_ipaddr', 
                  'logging_server_port', 
                  'logging_server_protocol', 
                  'logging_filename',
                  'logging_output_level',
                  'logging_cron_log_level')

class GenericIfStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenericIfStats
        fields = ('ifname',
                  'ifindex', 
                  'txBytes', 
                  'rxBytes', 
                  'txPkts', 
                  'rxPkts')
