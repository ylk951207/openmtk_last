#!/usr/bin/env python
import os
import docker
from common.log import *
from common.env import *
from common.request import *


def _get_docker_image_name(image_name, image_tag, registry):
    if registry:
        registry_ipaddr = registry['registryAddr']
        if registry_ipaddr:
            image_name = registry_ipaddr + "/" + image_name

    if image_tag:
        image_name = image_name + ":" + image_tag[0]

    log_info(LOG_MODULE_APNOTIFIER, "image_name(" + image_name + ")")
    return image_name

def docker_registry_proc(registry, params_dic):
    registry_certs = registry['registrySSLKey']

    if registry_certs:
        registry_addr = registry['registryAddr']
        certs_path = '/etc/docker/certs.d/' + registry_addr

        log_info(LOG_MODULE_REQUEST, "*** Create certs_path " + str(certs_path) + " ***")

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


def _docker_image_pull(client, noti_req, req_image):
    image_name = _get_docker_image_name(req_image['imageName'], req_image['imageTag'], req_image['registry'])

    noti_req.set_notification_value(image_name, 200, "Successful")

    if req_image['options']:
        params_dic = req_image['options']
    else:
        params_dic = dict()

    if req_image['registry']:
        params_dic = docker_registry_proc(req_image['registry'], params_dic)

        log_info(LOG_MODULE_REQUEST, "*** Parameters dictionary " + str(params_dic) + " ***")
    try:
        client.images.pull(image_name, **params_dic)
    except docker.errors.DockerException as e:
        log_error(LOG_MODULE_REQUEST, "*** client.images.pull() error: " + str(e))
        noti_req.set_notification_value(image_name, e.response.status_code, e)


def docker_image_create(request):
    noti_image_list = list()
    noti_req = APgentSendNotification()

    client = docker.from_env()
    log_info(LOG_MODULE_APNOTIFIER, "request: " + str(request))

    req_image_list = request["docker-image-list"]
    while len(req_image_list) > 0:
        req_image = req_image_list.pop(0)
        _docker_image_pull(client, noti_req, req_image)

    log_info(LOG_MODULE_REQUEST, "*** End image pull ***")

    log_info(LOG_MODULE_REQUEST, "noti_req : " + str(noti_req.response))
    # TODO after cAPC support this url
    #noti_req.send_notification(CAPC_NOTIFICATION_IMAGE_POST_URL)


def docker_cmd_proc(command, request):
    log_info(LOG_MODULE_APNOTIFIER, 'Received message: %s [request: %s]' % (command, str(request)))

    if command == SAL_PYTHON_DOCKER_IMAGE_CREATE:
        docker_image_create(request)
    else:
        log_info(LOG_MODULE_APNOTIFIER, 'Invalid Argument')