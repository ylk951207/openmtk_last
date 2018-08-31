from common.log import *

CONFIG_TYPE_SCALAR=1
CONFIG_TYPE_LIST=2


def pydata_get_section_map(config_name, *args):

  log_info(LOG_MODULE_SAL, "ARGS: " + str(args))

  if config_name == 'docker_image':
    section_map = {
      'loggingBufferSize'      :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_size'                 ,' ' ],
      'loggingServerIpAddr'    :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_ip'                   ,' ' ],
      'loggingServerPort'      :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_ip'                   ,' ' ],
      'loggingServerProtocol'  :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_proto'                ,' ' ],
      'loggingFilename'        :  [ CONFIG_TYPE_SCALAR  , 'system.@system[0].log_file'                 ,' ' ],
      'loggingOutputLevel'     :  [ CONFIG_TYPE_SCALAR  , ''                                           ,' ' ],
      'loggingCronLogLevel'    :  [ CONFIG_TYPE_SCALAR  , ''                                           ,' ' ],
    }
    return section_map

