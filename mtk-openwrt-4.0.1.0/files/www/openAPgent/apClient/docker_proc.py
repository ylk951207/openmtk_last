#!/usr/bin/env python
import os
import docker

from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *


LOG_MODULE_DOCKER_INIT="InitDocker"

def initialize_docker_containers():
    client = docker.from_env()
    container_list = client.containers.list(all=True)
    while container_list:
        container = container_list.pop()

        log_info(LOG_MODULE_DOCKER_INIT, "*** Docker container (%s) ***" % (container.name))

        try:
            container.stop()
        except docker.errors.DockerException as e:
            log_info(LOG_MODULE_DOCKER_INIT, "*** docker container '%s' stop error ***" %(container.name))
            log_info(LOG_MODULE_DOCKER_INIT, "*** error: " + str(e))

        log_info(LOG_MODULE_DOCKER_INIT, "*** Docker container (%s) stop done  ***" % (container.name))
        try:
            container.remove()
        except docker.errors.DockerException as e:
            log_info(LOG_MODULE_DOCKER_INIT, "*** docker container '%s' stop error ***" % (container.name))
            log_info(LOG_MODULE_DOCKER_INIT, "*** error: " + str(e))

        log_info(LOG_MODULE_DOCKER_INIT, "*** Docker container (%s) remove done  ***" % (container.name))

    log_info(LOG_MODULE_DOCKER_INIT, "*** Check container list  ***")
    container_list = client.containers.list(all=True)
    while container_list:
        container = container_list.pop()
        log_info(LOG_MODULE_DOCKER_INIT, "*** Cannot remove docker container (%s) ***" % (container.name))

    initialize_docker_container_iptables()


def initialize_docker_container_iptables():
    port_list = []
    wline = ""
    for key, src_port_list in MODULE_PORT_MAPPING_TABLE.items():
        for src_port in src_port_list:
            src_port = src_port.zfill(3)
            dest_port = "".join([DEST_PORT_PREFIX_PRIMARY, str(src_port)])
            port_list.append(dest_port)
            dest_port = "".join([DEST_PORT_PREFIX_SECONDARY, str(src_port)])
            port_list.append(dest_port)

    with open(FIREWALL_USER_FILE, 'r') as rfile:
        lines = rfile.readlines()

        for line in lines:
            line_skip = False
            token = line.split()
            if token:
                for port in port_list:
                    if token[-1] == str(port):
                        line_skip = True
                        break
            if line_skip == False:
                wline += line

    with open(TEMP_FIREWALL_USER_FILE, 'w') as wfile:
        wfile.write(wline)

    os.rename (TEMP_FIREWALL_USER_FILE, FIREWALL_USER_FILE)

    log_info(LOG_MODULE_DOCKER_INIT, "*** Docker container iptables Initialization Done (port:%s) ***" %(str(port_list)))
    '''
    Firewall restart will be executed by system_provisioning_done_proc() function.
    pmr._puci_default_module_restart("firewall")
    '''

def _get_docker_image_name(image_name, image_tag, registry):
    if registry:
        registry_ipaddr = registry['registryAddr']
        if registry_ipaddr:
            image_name = registry_ipaddr + "/" + image_name

    if image_tag:
        image_name = image_name + ":" + image_tag[0]

    log_info(LOG_MODULE_DOCKER, "image_name(" + image_name + ")")
    return image_name

def docker_registry_proc(registry, params_dic):
    registry_certs = registry['registrySSLKey']

    if registry_certs:
        registry_addr = registry['registryAddr']
        certs_path = '/etc/docker/certs.d/' + registry_addr

        log_info(LOG_MODULE_DOCKER, "*** Create certs_path " + str(certs_path) + " ***")

        if not os.path.exists(certs_path):
            os.makedirs(certs_path)

        f = open(certs_path+'/dockerCA.crt', 'w')
        f.write(registry_certs)
        f.close()

    auth_config = dict()
    if registry['registrySSLUser']:
        auth_config['username'] = registry['registrySSLUser']

    if registry['registrySSLPasswd']:
        auth_config['password'] = registry['registrySSLPasswd']

    params_dic['auth_config'] = auth_config
    return params_dic

def _docker_image_set_notification_value(noti_req, req_image):
    registry = req_image['registry']

    noti_req.response['imageName'] = req_image['imageName']
    noti_req.response['imageTag'] = req_image['imageTag']
    noti_req.response['imageDigest'] = req_image['imageDigest']
    noti_req.response['registryAddr'] = registry['registryAddr']
    device_identify = dict()
    device_identify['serialNumber'] = device_info_get_serial_num()
    noti_req.response['deviceIdentity'] = device_identify

    log_info(LOG_MODULE_DOCKER, "Set Notification body  = ", str(noti_req.response))


def _docker_image_pull(client, noti_req, req_image):
    registry = req_image['registry']
    image_name = _get_docker_image_name(req_image['imageName'], req_image['imageTag'], registry)

    _docker_image_set_notification_value (noti_req, req_image)

    if req_image['options']:
        params_dic = req_image['options']
    else:
        params_dic = dict()

    if registry:
        params_dic = docker_registry_proc(registry, params_dic)

        log_info(LOG_MODULE_DOCKER, "*** Parameters dictionary " + str(params_dic) + " ***")
    try:
        client.images.pull(image_name, **params_dic)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_DOCKER, "*** client.images.pull() error: " + str(e))
        noti_req.set_notification_value(e.response.status_code, e)


def _docker_image_remove(client, noti_req, req_image):
    params_dic = dict()
    registry = req_image['registry']
    image_name = _get_docker_image_name(req_image['imageName'], req_image['imageTag'], registry)
    log_info(LOG_MODULE_DOCKER, "Remove the previous image(%s)" % image_name)

    try:
        client.images.remove(image_name, **params_dic)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_DOCKER, "*** docker images.remove() error ***")
        log_error(LOG_MODULE_DOCKER, "*** error: " + str(e))
        if e.response.status_code != 404:
            noti_req.set_notification_value(e.response.status_code, e)

def docker_image_create_proc(request):
    client = docker.from_env()

    noti_req = APgentSendNotification()
    noti_req.set_notification_value(200, "Successful")

    '''
    if request['overwriteFlag'] == True:
        _docker_image_remove(client, noti_req, request)

    if noti_req.response['resultCode'] == 200:
    '''
    _docker_image_pull(client, noti_req, request)

    log_info(LOG_MODULE_DOCKER, "*** End image pull ***")

    noti_req.send_notification(CAPC_NOTIFICATION_IMAGE_POST_URL)
