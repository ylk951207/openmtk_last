import sys
import socket
import time
import docker
from common.log import *
from common.env import *
from common.request import *
from common.response import *

DOCKER_CREATE     = 1
DOCKER_DESTROY    = 2

'''
def send_request_apclient(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', APCLIENT_CMD_PORT))
    sock.send(str(data))
    sock.close()
    log_info(LOG_MODULE_SAL, "send_request_apclient() data: " + str(data))
def _docker_send_message_to_apclient(command, request):
    data = {
        'module' : "DOCKER",
        'command' : command,
        'body' : request
    }

    err = send_request_apclient (data)
    if err:
        log_info(LOG_MODULE_SAL, "send_request_apclient() result: " + err)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(LOG_MODULE_SAL, "Response = ", str(data))

    return data
'''


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
        image_data['imageTag'] = list()
        tags = image.tags
        for name in tags:
           if ':' in name:
              token = name.split(':')
              image_data['imageName'] = token[0]
              image_data['imageTag'].append(token[1])
           else:
              image_data['imageName'] = token[0]

        image_data['imageId'] = image.short_id
        history_dict = image.history()[0]
        image_data['createDate'] = history_dict['Created']
        image_data['size'] = history_dict['Size']

        image_data['imageDigest'] = ""
        image_data['options'] = ""
        image_data['trigger'] = ""

        registry = dict()
        registry['registryAddr'] = ""
        registry['registrySSLKey'] = ""
        registry['registrySSLUser'] = ""
        registry['registrySSLPasswd'] = ""
        image_data['registry'] = registry

        return image_data

    def _docker_registry_login(self, username, password):
        tls_config = docker.tls.TLSConfig(ca_cert='/root/docker/ca.pem')
        client = docker.DockerClient(base_url='unix://var/run/docker.sock', tls=tls_config)
        client.login(username='withusp', password='withusp', registry='https://192.168.1.191/v2/')

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
            image_name = _get_docker_image_name(req_image['imageName'], req_image['imageTag'], None)
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
        log_error(LOG_MODULE_SAL, "*** containers.get() error: " + str(e))
        docker_image.response.set_response_value(e.response.status_code, e, False)
        data = docker_image.response.make_response_body(None)
    else:
        while image_list:
            image = image_list.pop()
            image_data = docker_image._get_resp_data_from_image(image)
            image_data_list.append(image_data)
        data = {'docker-image-list' : image_data_list}
        data = docker_image.response.make_response_body(data)
    finally:
        return data

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
        data = docker_image.response.make_response_body(None)
    else:
        image_data = docker_image._get_resp_data_from_image(image)
        image_data_list.append(rc)
        data = {'docker-image' : image_data_list}
        data = docker_image.response.make_response_body(data)
    finally:
        return data


def py_docker_images_create(request):
    log_info(LOG_MODULE_SAL, "request: " + str(request))
    docker_image = DockerImageProc()
    docker_image.req_image_list = request["docker-image-list"]
    return docker_image._docker_image_create ()

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

    def _get_resp_data_from_container(self, container):
        container_data = dict()
        container_data['containerId'] = container.short_id
        container_data['containerName'] = container.name
        container_data['imageTag'] = list()
        tags = container.image.tags
        for name in tags:
           if ':' in name:
              token = name.split(':')
              container_data['imageName'] = token[0]
              container_data['imageTag'].append(token[1])
           else:
               container_data['imageName'] = token[0]
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
            params_dic['volumes'] = container['volumes']

        params_dic['detach'] = True

        log_info(LOG_MODULE_SAL, "container params_dic: " + str(params_dic))
        return params_dic

    def _docker_container_create(self):
        while len(self.req_container_list) > 0:
            req_container = self.req_container_list.pop(0)
            try:
                image_name = _get_docker_image_name(req_container['imageName'], req_container['imageTag'], req_container['registry'])
                if req_container['command']:
                    command_str = req_container['command']
                else:
                    command_str = None
                params_dic = self._docker_container_get_parameter_parse(req_container)
                self.client.containers.run(image_name, command_str, **params_dic)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_SAL, "*** docker container processing error ***")
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break

        return self.response.make_response_body(None)

    def _docker_container_mgt_proc(self, mgt_command, container, params_dic):
        log_info(LOG_MODULE_SAL, "Container : " + str(container) +
                 " (status:%s, name: %s)" % (str(container.status), str(container.name)))
        try:
            if mgt_command == 'start':
                container.start()
            elif mgt_command == 'stop':
                if params_dic:
                    container.stop(params_dic)
                else:
                    container.stop()
            elif mgt_command == 'restart':
                if params_dic:
                    container.restart(params_dic)
                else:
                    container.restart()
            elif mgt_command == 'remove':
                if params_dic:
                    container.remove(params_dic)
                else:
                    container.remove()
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

            try:
                mgt_command = req_container['command']
                container_name = req_container['containerName']
                container = self.client.containers.get(container_name)
            except docker.errors.DockerException as e:
                log_error(LOG_MODULE_SAL, "*** docker container processing(mgt_command:%s) error ***" %(mgt_command))
                log_error(LOG_MODULE_SAL, "*** error: " + str(e))
                self.response.set_response_value(e.response.status_code, e, False)
                break
            else:
                if req_container['options']:
                    params_dic = container['options']
                else:
                    params_dic = None
                self._docker_container_mgt_proc(mgt_command, container, **params_dic)

        return self.response.make_response_body(None)


def py_container_get_list():
    container_data_list = list()
    docker_container = DockerContainerProc()
    try:
            container_list = docker_container.client.containers.list(all=True)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_SAL, "*** containers.list() error: " + str(e))
        docker_container.response.set_response_value(e.response.status_code, e, False)
        data = docker_container.response.make_response_body(None)
    else:
        while container_list:
            container = container_list.pop()
            container_data = docker_container._get_resp_data_from_container(container)
            container_data_list.append(container_data)
        data = {'docker-container-list' : container_data_list}
        data = docker_container.response.make_response_body(data)
    finally:
        return data

def py_container_get_retrieve(container_name, add_header):
    container_data_list = list()
    docker_container = DockerContainerProc()
    try:
        container = docker_container.client.containers.get(container_name)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_SAL, "*** containers.get() error: " + str(e))
        docker_container.response.set_response_value(e.response.status_code, e, False)
        data = docker_container.response.make_response_body(None)
    else:
        container_data = docker_container._get_resp_data_from_container(container)
        container_data_list.append(container_data)
        data = {'docker-container' : container_data_list}
        data = docker_container.response.make_response_body(data)
    finally:
        return data

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


