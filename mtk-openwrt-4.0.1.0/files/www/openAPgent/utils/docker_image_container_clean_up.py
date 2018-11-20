import os
import docker

from common.env import *
from common.misc import *
from common.message import *
from common.sysinfo import *

def initialize_docker_containers():
    client = docker.from_env()
    container_list = client.containers.list(all=True)
    while container_list:
        container = container_list.pop()
        print ( "*** Docker container (%s) ***" % (container.name))
        try:
            container.stop()
        except docker.errors.DockerException as e:
            print ( "*** docker container '%s' stop error ***" %(container.name))
            print ( "*** error: " + str(e))

        print ( "*** Docker container (%s) stop done  ***" % (container.name))
        try:
            container.remove()
        except docker.errors.DockerException as e:
            print ( "*** docker container '%s' stop error ***" % (container.name))
            print ( "*** error: " + str(e))

        print ( "*** Docker container (%s) remove done  ***" % (container.name))

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
    print ("*** Docker container iptables Initialization Done (port:%s) ***" %(str(port_list)))


def initialize_docker_images():
    output, error = subprocess_open("docker images")
    print str(output)
    lines = output.splitlines()
    for line in lines:
        line = line.split()
        if 'REPOSITORY' in line:
            continue
        cmd_str = "docker rmi %s" %line[2]
        subprocess_open(cmd_str)
        print("Remove Image: " +  str(cmd_str))


initialize_docker_containers()
initialize_docker_images()