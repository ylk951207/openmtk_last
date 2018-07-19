"""apServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include
from rest_framework import routers
from apServer.server import views


class CustomRouter(routers.SimpleRouter):
    routes = [                                                       
        # List route.                                                     
        routers.Route(                                                  
            url=r'^{prefix}{trailing_slash}$',                  
            mapping={                                                  
                'get': 'list'          
            },                                   
            name='{basename}-list',                       
            initkwargs={'suffix': 'List'}     
        ),                                    
        # Dynamically generated list routes.  
        # Generated using @list_route decorator
        # on methods of the viewset.           
        routers.DynamicListRoute(                      
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',          
            initkwargs={}                                  
        ),                                                 
        # Detail route.                                    
        routers.Route(                                             
            url=r'^{prefix}/{lookup}{trailing_slash}$',    
            mapping={                                      
                'get': 'retrieve',    
                'post': 'create', 
                'put': 'update',
                'patch': 'partial_update',                 
                'delete': 'destroy'                                  
            }, 
            name='{basename}-detail',                                           
            initkwargs={'suffix': 'Instance'}          
        ),                                             
        # Dynamically generated detail routes.         
        # Generated using @detail_route decorator on methods of the viewset.
        routers.DynamicDetailRoute(                                                 
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',        
            name='{basename}-{methodnamehyphen}',                           
            initkwargs={}                                                   
        ),                                                                  
    ]                                                                       
     

'''
Define URL Patterns
'''
router = routers.DefaultRouter()
router.register(r'v1/devices', views.DeviceInfoViewSet)
# TODO: For the below, Support HTML handling like deviceInfo to validate the data without postman. (just for debugging)
router.register(r'v1/statistics/traffic', views.GenericIfStatsViewSet)


custom_router = CustomRouter()
custom_router.register(r'v1/interfaces', views.InterfaceConfigViewSet, base_name="interfaces")

system_config_list = views.SystemConfigViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update'
})


urlpatterns = [
    url(r'^v1/config/system/$', system_config_list, name='system-config-list'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += router.urls
urlpatterns += custom_router.urls

