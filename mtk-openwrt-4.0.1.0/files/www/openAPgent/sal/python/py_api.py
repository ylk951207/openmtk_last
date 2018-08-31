import docker
from common.log import *
from common.env import *
from common.response import *


def py_docker_download_detail_post(request, image_name):
    log_info(LOG_MODULE_SAL, "Image name: " + image_name)
    client = docker.from_env()
    image = client.images.pull(image_name)

    log_info(LOG_MODULE_SAL, "Image result: " + image)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(LOG_MODULE_SAL, "Response = ", str(data))

    return data

def py_container_creation_detail_post(request, image_name):
    client = docker.from_env()
    container = client.images.run(image_name, detach=True)
    log_info(LOG_MODULE_SAL, "Image result: " + container)

    data = {
        'header': {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    log_info(LOG_MODULE_SAL, "Response = ", str(data))

    return data

def py_docker_image_info():
    client = docker.from_env()
    for container in client.containers.list():
        log_info(LOG_MODULE_SAL, "Container: " + container)

def py_docker_container_stop():
    client = docker.from_env()
    for container in client.containers.list():
        container.stop()


