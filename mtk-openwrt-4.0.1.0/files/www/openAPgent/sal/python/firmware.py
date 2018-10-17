import fileinput
import os
import requests
from common.log import *
from common.env import *
from common.misc import *
from common.response import *

class FirmwareProc:
    def __init__(self):
        self.firmware_info_file = "/etc/openwrt_release"
        self.temp_image_file = "/tmp/firmware.img"

    def firmware_get_info(self):
        self.image_name_prefix = ""
        self.image_version = ""
        self.kernel_version = ""

        with open(self.firmware_info_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                token = line.split('=')
                token[1] = token[1].strip("\n,'")
                if token[0] == 'MTK_IMAGE_PREFIX':
                    self.image_name_prefix = token[1]
                elif token[0] == 'DISTRIB_RELEASE':
                    self.image_version = token[1]
                elif token[0] == 'MTK_KERNEL_VERSION':
                    self.kernel_version = token[1]

        info_data = dict()
        info_data['imageName'] = self.image_name_prefix + "_" + self.image_version + ".bin"
        info_data['version'] = self.image_version
        info_data['kernelVersion'] = self.kernel_version
        info_data['releaseDate'] = ""
        info_data['compileDate'] = ""
        info_data['bootloaderName'] = "u-boot-mtk_1.0.0.bin"
        info_data['bootloaderVersion'] = "v1.0.0"
        info_data['bootloaderReleaseDate'] = ""
        info_data['bootloaderCompileDate'] = ""
        return info_data

    #test url = 'https://speed.hetzner.de/100MB.bin'
    # https://docs.google.com/uc?export=download&id=1rTBsS_imzlj8uTVR_Obl0vumxkuqB7Kr
    def firmware_image_download(self, url):
        r = requests.get(url, allow_redirects=True)
        open(self.temp_image_file, 'wb').write(r.content)

    def firmware_image_supported(self, image_size):
        cmd_str = "sysupgrade -T %s >/dev/null" % self.temp_image_file
        output, error = subprocess_open(cmd_str)
        log_info("Firmware", "Execute '%s' command (output:%s, error:%s)" % (cmd_str, output, error))
        if "not found" in output:
            return -1

        file_size = os.stat(self.temp_image_file).st_size
        if file_size != image_size:
            return -1
        log_info("Firmware", "[filesize : %d]" %file_size)
        return 0

    def firmware_image_apply(self, keep_settings):
        if keep_settings == False:
            option = "-n"
        else:
            option = ""

        cmd_str = "sleep 1;killall dropbear uhttpd; sleep 1; /sbin/sysupgrade -d 2 %s '%s'" %(option, self.temp_image_file)
        output, error = subprocess_open(cmd_str)
        log_info("Firmware", "Execute '%s' command (output:%s, error:%s)" % (cmd_str, output, error))
        if error:
            return -1
        return 0

def py_firmware_management_list():
    firmware = FirmwareProc()
    data = {
        'firmware' : firmware.firmware_get_info(),
        'header' : {
            'resultCode': 200,
            'resultMessage': 'Success.',
            'isSuccessful': 'true'
        }
    }
    return data

def py_firmware_management_create(request):
    firmware = FirmwareProc()

    firmware.firmware_image_download(request['imagePath'])

    if firmware.firmware_image_supported(request['imageSize']) != 0:
        return response_make_simple_error_body(500, "Invalid image", None)

    firmware.firmware_image_apply(request['keepSettings'])

    return response_make_simple_success_body(None)


