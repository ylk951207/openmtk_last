from rest_framework import routers
from apServer.server import views

# If you need '/' as last character, refer to the below.
#			url=r'^{prefix}{trailing_slash}$',
class CustomRouter(routers.SimpleRouter):
	routes = [
		# List route.
		routers.Route(
			url=r'^{prefix}$',
			mapping={
				'get': 'list',
				'post': 'create',
				'put': 'update',
				'delete' : 'destroy',
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
			url=r'^{prefix}/{lookup}$',
			mapping={
				'get': 'retrieve',
				'post': 'detail_create',
				'put': 'detail_update',
				'patch': 'partial_update',
				'delete': 'delete_destroy'
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
		 

