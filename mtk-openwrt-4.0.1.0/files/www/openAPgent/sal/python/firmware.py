import fileinput
from common.log import *
from common.env import *
from common.response import *


def py_firmware_management_list():
    image_name_prefix = ""
    image_version = ""
    kernel_version = ""

    f = open ('/etc/openwrt_release', 'r')
    lines = f.readlines()
    for line in lines:
        token = line.split('=')
        token[1] = token[1].strip("\n,'")
        if token[0] == 'MTK_IMAGE_PREFIX':
            image_name_prefix = token[1]
        elif token[0] == 'DISTRIB_RELEASE':
            image_version = token[1]
        elif token[0] == 'MTK_KERNEL_VERSION':
            kernel_version = token[1]

    f.close()

    info_data = dict()
    info_data['imageName'] = image_name_prefix + "_" + image_version + ".bin"
    info_data['version'] = image_version
    info_data['kernelVersion'] = kernel_version
    info_data['releaseDate'] = ""
    info_data['compileDate'] = ""
    info_data['bootloaderName'] = "u-boot-mtk_1.0.0.bin"
    info_data['bootloaderVersion'] = "v1.0.0"
    info_data['bootloaderReleaseDate'] = ""
    info_data['bootloaderCompileDate'] = ""

    data = {
        'firmware' : info_data,
        'header' : {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def py_firmware_management_create(request):
    return response_make_simple_success_body(None)