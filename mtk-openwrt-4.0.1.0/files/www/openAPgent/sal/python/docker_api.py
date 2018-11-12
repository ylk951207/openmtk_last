import os
import docker

from common.env import *
from common.misc import *
from common.file import *
from common.message import *



def _get_docker_image_name(image_name, image_tag, registry):
    if registry:
        registry_ipaddr = registry['registryAddr']
        if registry_ipaddr:
            image_name = registry_ipaddr + "/" + image_name

    if image_tag:
        image_name = image_name + ":" + image_tag[0]

    log_info(LOG_MODULE_DOCKER, "image_name(" + image_name + ")")
    return image_name


class DockerImageProc():
    def __init__(self):
        self.client = docker.from_env()
        self.response = APgentResponseMessgae()
        self.response.set_response_value(200, "Successful", True)

    def _get_resp_data_from_image(self, image):
        image_data = dict()
        registry = dict()

        image_data['imageTag'] = list()
        tags = image.tags
        for name in tags:
            token = name.split('/')
            if '/' in name:
                registry['registryAddr'] = token[0]
                name = token[1]
            if ':' in name:
              token = name.split(':')
              image_data['imageName'] = token[0]
              image_data['imageTag'].append(token[1])
            else:
              image_data['imageName'] = name

        #image_data['imageId'] = image.attrs['Id'].split(':')[1][0:12]
        image_data['imageId'] = image.attrs['Id'][7:19]
        history_dict = image.history()[0]
        image_data['createDate'] = history_dict['Created']
        image_data['size'] = image.attrs['Size']
        log_debug(LOG_MODULE_DOCKER, "Image Id : %s, size : %s" %(str(image_data['imageId']), str(image_data['size'])))

        image_data['imageDigest'] = ""
        image_data['options'] = ""
        image_data['trigger'] = ""


        registry['registrySSLKey'] = ""
        registry['registrySSLUser'] = ""
        registry['registrySSLPasswd'] = ""
        image_data['registry'] = registry

        return image_data

    def _docker_image_create(self):
        while len(self.req_image_list) > 0:
            req_image = self.req_image_list.pop(0)
            image_name = _get_docker_image_name(req_image['imageName'], req_image['imageTag'], req_image['registry'])
            if req_image['options']:
                params_dic = req_image['options']
            else:
                params_dic = dict()

            try:
                self.client.images.pull(image_name)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_DOCKER, "*** docker image processing(create) error ***")
                log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break

        return self.response.make_response_body(None)

    def _docker_image_destroy(self):
        while len(self.req_image_list) > 0:
            req_image = self.req_image_list.pop(0)
            image_name = _get_docker_image_name(req_image['imageName'], req_image['imageTag'], req_image['registry'])
            if req_image['options']:
                params_dic = req_image['options']
            else:
                params_dic = dict()

            try:
                self.client.images.remove(image_name, **params_dic)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_DOCKER, "*** docker image processing(destroy) error ***")
                log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break

        return self.response.make_response_body(None)

def py_docker_images_list():
    image_data_list = list()
    docker_image = DockerImageProc()
    try:
        image_list = docker_image.client.images.list()
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_DOCKER, "*** images.get() error: " + str(e))
        docker_image.response.set_response_value(e.response.status_code, e, False)
        return docker_image.response.make_response_body(None)
    else:
        while image_list:
            image = image_list.pop()
            image_data = docker_image._get_resp_data_from_image(image)
            image_data_list.append(image_data)
        data = {'docker-image-list' : image_data_list}
        return docker_image.response.make_response_body(data)

'''
image_name : image_name:tag_name or 
'''
def py_docker_images_retrieve(image_name, add_header):
    image_data_list = list()
    docker_image = DockerImageProc()

    try:
        image = docker_image.client.images.get(image_name)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_DOCKER, "*** containers.get() error: " + str(e))
        docker_image.response.set_response_value(e.response.status_code, e, False)
        return docker_image.response.make_response_body(None)
    else:
        image_data = docker_image._get_resp_data_from_image(image)
        image_data_list.append(image_data)
        data = {'docker-image' : image_data_list}
        return docker_image.response.make_response_body(data)

def py_docker_images_create(request):
    server_msg = ApServerLocalMassage(APNOTIFIER_CMD_PORT)

    req_image_list = request["docker-image-list"]
    while len(req_image_list) > 0:
        req_image = req_image_list.pop(0)
        server_msg.send_message_to_apnotifier(SAL_PYTHON_DOCKER_IMAGE_CREATE, req_image)

    return response_make_simple_success_body(None)

'''
TODO: Temporary processing 
If pk is 'delete', call destroy function.
'''
def py_docker_images_detail_create(request, pk):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))

    if pk == 'delete':
        docker_image = DockerImageProc()
        docker_image.req_image_list = request["docker-image-list"]
        return docker_image._docker_image_destroy()

    '''
    docker_image = DockerImageProc()
    docker_image.req_image_list = list()
    docker_image.req_image_list.append(request)
    return docker_image._docker_image_create()
    '''

def py_docker_images_destroy(request):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))
    docker_image = DockerImageProc()
    docker_image.req_image_list = request["docker-image-list"]
    return docker_image._docker_image_destroy ()

def py_docker_images_detail_destroy(request, pk):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))
    docker_image = DockerImageProc()
    docker_image.req_image_list = list()
    docker_image.req_image_list.append(request)
    return docker_image._docker_image_destroy()

class DockerContainerProc():
    def __init__(self):
        self.client = docker.from_env()
        self.response = APgentResponseMessgae()
        self.response.set_response_value(200, "Successful", True)
        self.prev_container_name=None

    def _get_resp_data_from_container(self, container):
        container_data = dict()
        container_data['containerId'] = container.short_id
        container_data['containerName'] = container.name
        container_data['imageTag'] = list()
        tags = container.image.tags
        container_data['imageFullName'] = tags[0]
        registryAddr = ""
        for name in tags:
           token = name.split('/')
           if '/' in name:
               registryAddr = token[0]
               name = token[1]
           if ':' in name:
              token = name.split(':')
              #image_name = registryAddr + "/" + token[0]
              image_name = token[0]
              container_data['imageName']= image_name
              container_data['imageTag'].append(token[1])
           else:
               # image_name = registryAddr + "/" + name
               container_data['imageName'] = name
        container_data['command'] = ""
        container_data['created'] = container.attrs['Created'].split(".")[0].replace('T', ' ')
        container_data['status'] = container.status
        container_data['ports'] = list()
        return container_data

    def _docker_container_get_parameter_parse(self, container, dest_port_list):
        '''
         container['options'] is dictionary type.
        '''
        if container['options']:
            params_dic = container['options']
        else:
            params_dic = dict()

        if container['containerName']:
            params_dic['name'] = container['containerName']
        if container['ports']:
            params_dic['ports'] = container['ports']
        if container['volumes']:
           volumes_list =  container['volumes']
           volume_param_data = dict()
           while volumes_list:
               volume = volumes_list.pop(0)
               sub_data = {
                    'bind' : volume['bind'],
                    'mode' : volume['mode']
               }
               volume_param_data[volume['dir']] = sub_data
           params_dic['volumes'] = volume_param_data

        params_dic['detach'] = True
        if container['command']:
            params_dic['command'] = container['command']
        else:
            params_dic['command'] = None

        if len(dest_port_list) > 0:
            params_dic['environment'] = {'ARGS' : " ".join(dest_port_list)}

        log_info(LOG_MODULE_DOCKER, "container params_dic: " + str(params_dic))
        return params_dic

    def _docker_container_get_by_image_name(self, container_name):
        name_prefix = container_name.split('_')[0]
        cmd_str = "docker ps -a --filter 'name=" + name_prefix + "' | grep " + name_prefix + " | awk '{print $NF}'"
        output, error = subprocess_open(cmd_str)
        output = output.split()
        log_info(LOG_MODULE_DOCKER, "Execute command(%s) output:%s, error:%s ***" % (str(cmd_str), str(output), str(error)))
        if not error:
            return output
        return None

    def _docker_get_previous_run_container(self, container_name):
        prev_container_list = self._docker_container_get_by_image_name(container_name)
        if prev_container_list == None: return None

        for i in range(0, len(prev_container_list)):
            prev_container_name = prev_container_list[i].strip()

            if container_name == prev_container_name:
                log_info(LOG_MODULE_DOCKER, "Skip the same container %s" %(prev_container_name))
                continue

            # This is not created by cAPC with the correct procedure
            if not "_" in prev_container_name:
                continue

            try:
                prev_container = self.client.containers.get(prev_container_name)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_DOCKER, "*** docker previous container get() error for %s ***" %prev_container_name)
                log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
            else:
                log_info(LOG_MODULE_DOCKER, "Get the previous container '%s' info (status:%s)" % (prev_container_name, prev_container.status))
                return prev_container

        return None


    def _docker_container_get_by_name(self, container_name):
        if not container_name: return None
        container_name = container_name.strip()
        log_info(LOG_MODULE_DOCKER, "Get container by container_name: " + container_name)

        try:
            container = self.client.containers.get(container_name)
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_DOCKER, "*** docker container rollback() error")
            log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
            return None

        return container

    def _docker_container_remove_unused_container(self, prev_container, error, dest_port_list):
        if prev_container:
            log_info(LOG_MODULE_DOCKER, "prev_continer exist")
            prev_dest_port_list = []
            for dest_port in dest_port_list:
                src_port = dest_port[2:]

                if dest_port[:2] == DEST_PORT_PREFIX_PRIMARY:
                    prev_dest_port_list.append(DEST_PORT_PREFIX_SECONDARY + src_port)
                else:
                    prev_dest_port_list.append(DEST_PORT_PREFIX_PRIMARY + src_port)

            mgt_command = "stop"
            self._docker_container_mgt_proc(mgt_command, prev_container, None, None)

            mgt_command = "remove"
            self._docker_container_mgt_proc(mgt_command, prev_container, prev_dest_port_list, None)
            log_info(LOG_MODULE_DOCKER, "Remove the deprecated containers for %s" % prev_container.name)

    def _docker_container_iptables_proc(self, prev_container, dest_port_list, is_add):
        log_info(LOG_MODULE_DOCKER, "iptables port list: " + str(dest_port_list))

        del_cmd_list = []
        add_cmd_list = []
        wline = ""

        for dest_port in dest_port_list:
            src_temp_port = dest_port[2:]
            if src_temp_port[0] == '0':
                src_port = src_temp_port[1:]
            else:
                src_port = src_temp_port

            if is_add:
                #if dest_port[:2] == DEST_PORT_PREFIX_PRIMARY:
                prev_dest_port_list = [DEST_PORT_PREFIX_SECONDARY + src_temp_port, DEST_PORT_PREFIX_PRIMARY + src_temp_port]

                for prev_dest_port in prev_dest_port_list:
                    cmd_str = "iptables -t nat -I PREROUTING -p TCP --dport %s -j REDIRECT --to-port %s" % (src_port, prev_dest_port)
                    del_cmd_list.append(cmd_str)
                    cmd_str = "iptables -t nat -I PREROUTING -p UDP --dport %s -j REDIRECT --to-port %s" % (src_port, prev_dest_port)
                    del_cmd_list.append(cmd_str)

                cmd_str = "iptables -t nat -I PREROUTING -p TCP --dport %s -j REDIRECT --to-port %s" % (src_port, dest_port)
                add_cmd_list.append(cmd_str)
                cmd_str = "iptables -t nat -I PREROUTING -p UDP --dport %s -j REDIRECT --to-port %s" % (src_port, dest_port)
                add_cmd_list.append(cmd_str)
            else:
                cmd_str = "iptables -t nat -I PREROUTING -p TCP --dport %s -j REDIRECT --to-port %s" % (src_port, dest_port)
                del_cmd_list.append(cmd_str)
                cmd_str = "iptables -t nat -I PREROUTING -p UDP --dport %s -j REDIRECT --to-port %s" % (src_port, dest_port)
                del_cmd_list.append(cmd_str)

        log_info(LOG_MODULE_APCLIENT, "add_cmd_list : " + str(add_cmd_list))
        log_info(LOG_MODULE_APCLIENT, "del_cmd_list : " + str(del_cmd_list))

        with open(FIREWALL_USER_FILE, 'r') as rfile:
            lines = rfile.readlines()

            for line in lines:
                skip_line = False
                for cmd_str in del_cmd_list:
                    if cmd_str in line:
                        skip_line = True

                if skip_line == False:
                    wline += line

        if wline:
            with open(TEMP_FIREWALL_USER_FILE, 'w') as wfile:
                wfile.write(wline)

                for cmd_str in add_cmd_list:
                    wfile.write(cmd_str + "\n")

            os.rename (TEMP_FIREWALL_USER_FILE, FIREWALL_USER_FILE)
            output, error = subprocess_open("/etc/init.d/firewall restart")

            log_info(LOG_MODULE_APCLIENT, "== /etc/init.d firewall restart Done == ")

    def _get_docker_container_available_port(self, container_prefix):
        dest_port_list = []

        for key, src_port_list in MODULE_PORT_MAPPING_TABLE.items():
            if container_prefix != key:
                continue

            for src_port in src_port_list:
                # TOOD: not found dest port
                src_port = src_port.zfill(3)
                dest_port = "".join([DEST_PORT_PREFIX_PRIMARY, str(src_port)])
                if self._check_docker_container_iptables_port(dest_port) == True:
                    dest_port_list.append(dest_port)
                else:
                    dest_port = "".join([DEST_PORT_PREFIX_SECONDARY, str(src_port)])
                    dest_port_list.append(dest_port)

            if len(dest_port_list) <= 0:
                dest_port_list = src_port_list

        log_info(LOG_MODULE_DOCKER, "container(%s) dest_port_list[%s]" %(container_prefix, str(dest_port_list)))
        return dest_port_list

    def _check_docker_container_iptables_port(self, port_number):
        log_info(LOG_MODULE_DOCKER, "Check the available container port_number(" + port_number + ")")
        cmd_str = "iptables -t nat -L | grep %s" %port_number
        output, error = subprocess_open(cmd_str)

        output = output.split()
        if port_number in output and output[-1] == port_number:
            # Port number already exist
            log_info(LOG_MODULE_DOCKER, "Port number already exist")
            return False
        else:
            log_info(LOG_MODULE_DOCKER, "Port number is available")
            return True

    def _docker_container_remove_failed_container(self, container_name):
        log_info(LOG_MODULE_DOCKER, "*** docker %s continaer remove as failure ***" % (container_name))
        try:
            container = self.client.containers.get(container_name)
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_DOCKER,
                      "*** docker %s container processing error ***" %(container_name))
            log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
            return

        log_error(LOG_MODULE_DOCKER,
                  "*** Clean up the failed container(%s) ***" % (container.name))
        try:
            container.stop()
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_DOCKER,
                      "*** docker %s container STOP processing error ***" % (container.name))
            log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
            return

        try:
            container.remove()
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_DOCKER,
                      "*** docker %s container REMOVE processing error ***" % (container.name))
            log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
            return

    def _docker_container_create(self):
        error = False
        resp_body = dict()
        resp_body['rollback'] = {
            'rollbackFlag' : False,
            'rollbackContainer' : ""
        }

        while len(self.req_container_list) > 0:
            req_container = self.req_container_list.pop(0)

            lock = FileLock("container_lock", dir="/tmp")
            lock.acquire()

            prev_container = self._docker_get_previous_run_container(req_container['containerName'])
            image_name = _get_docker_image_name(req_container['imageName'], req_container['imageTag'],
                                                req_container['registry'])
            dest_port_list = self._get_docker_container_available_port(req_container['imageName'])
            params_dic = self._docker_container_get_parameter_parse(req_container, dest_port_list)

            try:
                self.client.containers.run(image_name, **params_dic)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_DOCKER, "*** docker containers.run() error ***")
                log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)

                # Error 409 is conflict name error
                if e.response.status_code == 409:
                    # Conflict name error, Do not remove the current container and response with rollback info.
                    resp_body['rollback'] = {
                        'rollbackFlag': True,
                        'rollbackContainer': req_container['containerName']
                    }
                else:
                    error = True
                    # If the previous container exists, Make response with rollback info.
                    if prev_container:
                        resp_body['rollback'] = {
                            'rollbackFlag': True,
                            'rollbackContainer': prev_container.name
                        }

                    if error == True:
                        self._docker_container_remove_failed_container(req_container['containerName'])
                break
            else:
                log_info(LOG_MODULE_DOCKER, "containers.run() success for %s" %image_name)
                self._docker_container_iptables_proc(prev_container, dest_port_list, True)

        if error == False:
            self._docker_container_remove_unused_container(prev_container, error, dest_port_list)
        log_info(LOG_MODULE_DOCKER, "rollback data : " + str(resp_body))

        lock.release()

        return self.response.make_response_body(resp_body)

    def _docker_container_remove_iptables_proc(self, container_name, dest_port_list):
        container_prefix = container_name.split("_")[0]

        if dest_port_list:
            self._docker_container_iptables_proc(None, dest_port_list, False)
        else:
            port_list = []
            for key, src_port_list in MODULE_PORT_MAPPING_TABLE.items():
                if container_prefix != key:
                    continue

                for src_port in src_port_list:
                    src_port = src_port.zfill(3)
                    port_list.append("".join([DEST_PORT_PREFIX_PRIMARY, str(src_port)]))
                    port_list.append("".join([DEST_PORT_PREFIX_SECONDARY, str(src_port)]))

                self._docker_container_iptables_proc(None, port_list, False)

    def _docker_container_mgt_proc(self, mgt_command, container, dest_port_list, options):
        if options:
            params_dic = options
        else:
            params_dic = dict()

        log_info(LOG_MODULE_DOCKER, "Container : " + str(container) +
                 " (status:%s, name: %s) <- command %s" % (str(container.status), str(container.name), mgt_command))
        try:
            if mgt_command == 'start':
                container.start()
            elif mgt_command == 'stop':
                if params_dic:
                    container.stop(**params_dic)
                else:
                    container.stop()
            elif mgt_command == 'restart':
                if params_dic:
                    container.restart(**params_dic)
                else:
                    container.restart()
            elif mgt_command == 'remove':
                if params_dic:
                    container.remove(**params_dic)
                else:
                    container.remove()

                self._docker_container_remove_iptables_proc(container.name, dest_port_list)
            elif mgt_command == 'stop-remove':
                if params_dic:
                    container.stop(**params_dic)
                else:
                    container.stop()

                if params_dic:
                    container.remove(**params_dic)
                else:
                    container.remove()

                self._docker_container_remove_iptables_proc(container.name, dest_port_list)
            elif mgt_command == 'rename':
                container.rename(params_dic['rename'])
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_DOCKER, "*** docker container processing error(%s) ***" %mgt_command)
            log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
            self.response.set_response_value(e.response.status_code, e, False)
            return e.response.status_code
        finally:
            log_info(LOG_MODULE_DOCKER, "_docker_container_mgt_proc() : " + mgt_command + " Done..")
            return 200

    def _docker_container_management(self):
        while len(self.req_container_list) > 0:
            req_container = self.req_container_list.pop(0)

            # TODO : docker container exist check and remove

            try:
                mgt_command = req_container['command']
                container_name = req_container['containerName']
                container = self.client.containers.get(container_name)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_DOCKER, "*** docker container processing(mgt_command:%s) error ***" %(str(mgt_command)))
                log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break
            else:
                self._docker_container_mgt_proc(mgt_command, container, None, req_container['options'])

        return self.response.make_response_body(None)


def py_container_get_list():
    container_data_list = list()
    docker_container = DockerContainerProc()
    try:
            container_list = docker_container.client.containers.list(all=True)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_DOCKER, "*** containers.list() error: " + str(e))
        docker_container.response.set_response_value(e.response.status_code, e, False)
        return docker_container.response.make_response_body(None)
    else:
        while container_list:
            container = container_list.pop()
            container_data = docker_container._get_resp_data_from_container(container)
            container_data_list.append(container_data)
        data = {'docker-container-list' : container_data_list}
        return docker_container.response.make_response_body(data)

def py_container_get_retrieve(container_name, add_header):
    container_data_list = list()
    docker_container = DockerContainerProc()
    try:
        container = docker_container.client.containers.get(container_name)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_DOCKER, "*** containers.get() error: " + str(e))
        docker_container.response.set_response_value(e.response.status_code, e, False)
        return docker_container.response.make_response_body(None)
    else:
        container_data = docker_container._get_resp_data_from_container(container)
        container_data_list.append(container_data)
        data = {'docker-container' : container_data_list}
        return docker_container.response.make_response_body(data)

def py_container_creation_create(request):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = request["docker-container-list"]
    return docker_container._docker_container_create ()

def py_container_creation_detail_create(request, pk):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = list()
    docker_container.req_container_list.append(request)
    return docker_container._docker_container_create()

def py_container_management_create(request):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = request["docker-container-list"]
    return docker_container._docker_container_management()

def py_container_management_detail_create(request, pk):
    log_info(LOG_MODULE_DOCKER, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = list()
    docker_container.req_container_list.append(request)
    return docker_container._docker_container_management()


