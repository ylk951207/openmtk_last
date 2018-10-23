#!/usr/bin/python
import docker

from common.misc import *


LOG_MODULE_DOCKER_INIT="InitDocker"

def init_docker_docker_container():
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
        log_info(LOG_MODULE_DOCKER_INIT, "*** Docker container (%s) ***" % (container.name))

