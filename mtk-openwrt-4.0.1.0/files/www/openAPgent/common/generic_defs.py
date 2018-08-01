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
		 




def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


