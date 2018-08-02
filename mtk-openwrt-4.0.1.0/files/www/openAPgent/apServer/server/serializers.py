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

