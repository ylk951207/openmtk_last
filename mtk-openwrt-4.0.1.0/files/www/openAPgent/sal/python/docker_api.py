import docker
import subprocess

from common.log import *
from common.env import *
from common.request import *
from common.response import *

def subprocess_open(command):
	popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(stdoutdata, stderrdata) = popen.communicate()
	return stdoutdata, stderrdata

def _get_docker_image_name(image_name, image_tag, registry):
    if registry:
        registry_ipaddr = registry['registryAddr']
        if registry_ipaddr:
            image_name = registry_ipaddr + "/" + image_name

    if image_tag:
        image_name = image_name + ":" + image_tag[0]

    log_info(LOG_MODULE_SAL, "image_name(" + image_name + ")")
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

        image_data['imageId'] = image.short_id
        history_dict = image.history()[0]
        image_data['createDate'] = history_dict['Created']
        image_data['size'] = history_dict['Size']

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
                log_error(LOG_MODULE_SAL, "*** docker image processing(create) error ***")
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
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
                log_error(LOG_MODULE_SAL, "*** docker image processing(destroy) error ***")
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break

        return self.response.make_response_body(None)

def py_docker_images_list():
    image_data_list = list()
    docker_image = DockerImageProc()
    try:
        image_list = docker_image.client.images.list()
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_SAL, "*** images.get() error: " + str(e))
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
        log_error(LOG_MODULE_SAL, "*** containers.get() error: " + str(e))
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
        server_msg.send_message_to_apnotifier("DOCKER", SAL_PYTHON_DOCKER_IMAGE_CREATE, req_image)

    return response_make_simple_success_body()

def py_docker_images_detail_create(request, pk):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_image = DockerImageProc()
    docker_image.req_image_list = list()
    docker_image.req_image_list.append(request)
    return docker_image._docker_image_create()

def py_docker_images_destroy(request):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_image = DockerImageProc()
    docker_image.req_image_list = request["docker-image-list"]
    return docker_image._docker_image_destroy ()

def py_docker_images_detail_destroy(request, pk):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
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
        container_data['created'] = ""
        container_data['status'] = container.status
        container_data['ports'] = list()
        return container_data

    def _docker_container_get_parameter_parse(self, container):
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
            params_dic['command'] = "/start.sh"

        log_info(LOG_MODULE_SAL, "container params_dic: " + str(params_dic))
        return params_dic

    def _docker_container_get_by_image_name(self, container_name):
        name_prefix = container_name.strip('_')[0]
        cmd_str = "docker ps -a --filter 'name=" + name_prefix + "' | grep " + name_prefix + " | awk '{print $NF}'"
        output, error = subprocess_open(cmd_str)
        output = output.split()
        log_info(LOG_MODULE_SAL, "Execute command(%s) output(%s) error(%s)***" % (str(cmd_str), str(output), str(error)))
        if not error:
            return output
        return None

    def _docker_container_stop_previous(self, req_container):
        if not "containerName" in req_container: return None

        prev_container_list = self._docker_container_get_by_image_name(req_container['containerName'])
        if prev_container_list == None: return None

        for i in range(0, len(prev_container_list)):
            prev_container_name = prev_container_list[i]
            prev_container_name.strip()

            log_info(LOG_MODULE_SAL, "Previous container name %s Stop " %(str(prev_container_name)))

            try:
                prev_container = self.client.containers.get(prev_container_name)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_SAL, "*** docker previous container stop() error ***")
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
                return e.response.status_code
            else:
                mgt_command = "stop"
                self._docker_container_mgt_proc(mgt_command, prev_container, None)
                self.prev_container_name = prev_container.name

                '''
                if prev_container.name == req_container['containerName']:
                    if req_container['replaceField']:
                        log_error(LOG_MODULE_SAL, "Remove the duplicated container")
                        mgt_command = "rename"
                        params = {"rename" : prev_container.name + ".old"}
                        log_info(LOG_MODULE_SAL, "Rename container %s --> %s" % prev_container.name, prev_container.name + ".old")
                        self._docker_container_mgt_proc(mgt_command, prev_container, params)
                        self.prev_container_name = prev_container.name + ".old"
                '''

                log_info(LOG_MODULE_SAL, "Current - previous container - is %s" %self.prev_container_name)

    def _docker_container_get_previous(self):
        if not self.prev_container_name: return None
        log_info(LOG_MODULE_SAL, "Previous container Restart, prev_container_name:" + self.prev_container_name)
        self.prev_container_name.strip()

        try:
            prev_container = self.client.containers.get(self.prev_container_name)
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_SAL, "*** docker container rollback() error")
            log_error(LOG_MODULE_SAL, "*** error: " + str(e))
            return None

        return prev_container

    def _docker_container_rollback_previous(self):
        prev_container = self._docker_container_get_previous()
        if prev_container:
            mgt_command = "rename"
            token = prev_container.name.split('.')
            params = {"rename": token[0]}
            log_info(LOG_MODULE_SAL, "Rename container %s --> %s" %prev_container.name, token[0])
            self._docker_container_mgt_proc(mgt_command, prev_container, params)
            mgt_command = "restart"
            self._docker_container_mgt_proc(mgt_command, prev_container, None)

    def _docker_container_remove_previous(self):
        prev_container = self._docker_container_get_previous()
        if prev_container:
            log_info(LOG_MODULE_SAL, "Remove previous container %s" % prev_container.name)
            mgt_command = "stop"
            self._docker_container_mgt_proc(mgt_command, prev_container, None)
            mgt_command = "remove"
            self._docker_container_mgt_proc(mgt_command, prev_container, None)

    def _docker_container_create(self):
        while len(self.req_container_list) > 0:
            req_container = self.req_container_list.pop(0)

            self._docker_container_stop_previous(req_container)

            try:
                image_name = _get_docker_image_name(req_container['imageName'], req_container['imageTag'], req_container['registry'])
                params_dic = self._docker_container_get_parameter_parse(req_container)

                self.client.containers.run(image_name, **params_dic)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_SAL, "*** docker container processing error ***")
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                self._docker_container_rollback_previous()
                break
            else:
                log_info(LOG_MODULE_SAL, "containers.run() success for %s" %image_name)
                self._docker_container_remove_previous()

        return self.response.make_response_body(None)

    def _docker_container_mgt_proc(self, mgt_command, container, options):
        if options:
            params_dic = options
        else:
            params_dic = dict()

        log_info(LOG_MODULE_SAL, "Container : " + str(container) +
                 " (status:%s, name: %s)" % (str(container.status), str(container.name)))
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
            elif mgt_command == 'rename':
                container.remove(params_dic['rename'])
        except docker.errors.DockerException as e:
            log_error(LOG_MODULE_SAL, "*** docker container processing error(%s) ***" %mgt_command)
            log_error(LOG_MODULE_SAL, "*** error: " + str(e))
            self.response.set_response_value(e.response.status_code, e, False)
        finally:
            log_info(LOG_MODULE_SAL, "_docker_container_mgt_proc() : " + mgt_command + " Done..")
            # error

    def _docker_container_management(self):
        while len(self.req_container_list) > 0:
            req_container = self.req_container_list.pop(0)

            # TODO : docker container exist check and remove

            try:
                mgt_command = req_container['command']
                container_name = req_container['containerName']
                container = self.client.containers.get(container_name)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_SAL, "*** docker container processing(mgt_command:%s) error ***" %(str(mgt_command)))
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break
            else:
                self._docker_container_mgt_proc(mgt_command, container, req_container['options'])

        return self.response.make_response_body(None)


def py_container_get_list():
    container_data_list = list()
    docker_container = DockerContainerProc()
    try:
            container_list = docker_container.client.containers.list(all=True)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_SAL, "*** containers.list() error: " + str(e))
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
        log_error(LOG_MODULE_SAL, "*** containers.get() error: " + str(e))
        docker_container.response.set_response_value(e.response.status_code, e, False)
        return docker_container.response.make_response_body(None)
    else:
        container_data = docker_container._get_resp_data_from_container(container)
        container_data_list.append(container_data)
        data = {'docker-container' : container_data_list}
        return docker_container.response.make_response_body(data)

def py_container_creation_create(request):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = request["docker-container-list"]
    return docker_container._docker_container_create ()

def py_container_creation_detail_create(request, pk):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = list()
    docker_container.req_container_list.append(request)
    return docker_container._docker_container_create()

def py_container_management_create(request):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = request["docker-container-list"]
    return docker_container._docker_container_management()

def py_container_management_detail_create(request, pk):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_container = DockerContainerProc()
    docker_container.req_container_list = list()
    docker_container.req_container_list.append(request)
    return docker_container._docker_container_management()


