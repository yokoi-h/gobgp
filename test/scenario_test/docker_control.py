# Copyright (C) 2014 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fabric.api import local
import re
import os

GOBGP_CONTAINER_NAME = "gobgp"
GOBGP_ADDRESS = "10.0.255.1/16"
GOBGP_CONFIG_FILE = "gobgpd.conf"
EXABGP_CONTAINER_NAME = "exabgp"
EXABGP_ADDRESS = "10.0.0.100/16"
EXABGP_CONFDIR = "/etc/exabgp/"
EXABGP_LOG_FILE = "exabgpd.log"
BRIDGE_ADDRESS = "10.0.255.2"
CONFIG_DIR = "/usr/local/gobgp"
CONFIG_DIRR = "/usr/local/gobgp/"
CONFIG_DIRRR = "/usr/local/gobgp/*"
STARTUP_FILE_NAME = "gobgp_startup.sh"
STARTUP_FILE = "/mnt/" + STARTUP_FILE_NAME
BRIDGE_0 = {"BRIDGE_NAME": "br0", "BRIDGE_ADDRESS": "10.0.255.2"}
BRIDGE_1 = {"BRIDGE_NAME": "br1", "BRIDGE_ADDRESS": "11.0.255.2"}
BRIDGE_2 = {"BRIDGE_NAME": "br2", "BRIDGE_ADDRESS": "12.0.255.2"}
BRIDGES = [BRIDGE_0, BRIDGE_1, BRIDGE_2]
A_PART_OF_CURRENT_DIR = "/test/scenario_test"


def test_user_check():
    root = False
    outbuf = local("echo $USER", capture=True)
    user = outbuf
    if user == "root":
        root = True

    return root


def install_docker_and_tools():
    print "start install packages of test environment."
    if test_user_check() is False:
        print "you are not root"
        return

    local("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys "
          "36A1D7869245C8950F966E92D8576A8BA88D21E9", capture=True)
    local('sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"',
          capture=True)
    local("apt-get update", capture=True)
    local("apt-get install -y --force-yes lxc-docker-1.3.2", capture=True)
    local("ln -sf /usr/bin/docker.io /usr/local/bin/docker", capture=True)
    local("gpasswd -a `whoami` docker", capture=True)
    local("apt-get install -y --force-yes emacs23-nox", capture=True)
    local("apt-get install -y --force-yes wireshark", capture=True)
    local("apt-get install -y --force-yes iputils-arping", capture=True)
    local("apt-get install -y --force-yes bridge-utils", capture=True)
    local("apt-get install -y --force-yes tcpdump", capture=True)
    local("apt-get install -y --force-yes lv", capture=True)
    local("wget https://raw.github.com/jpetazzo/pipework/master/pipework -O /usr/local/bin/pipework",
          capture=True)
    local("chmod 755 /usr/local/bin/pipework", capture=True)
    local("docker pull osrg/quagga", capture=True)
    local("docker pull osrg/gobgp", capture=True)
    local("docker pull osrg/exabgp", capture=True)
    local("mkdir /usr/local/gobgp", capture=True)


def docker_pkg_check():
    docker_exists = False
    outbuf = local("dpkg -l | grep docker | awk '{print $2}'", capture=True)
    dpkg_list = outbuf.split('\n')
    for dpkg in dpkg_list:
        if "lxc-docker" in dpkg:
            docker_exists = True
    return docker_exists


def go_path_check():
    go_path_exist = False
    outbuf = local("echo `which go`", capture=True)
    if "go" in outbuf:
        go_path_exist = True
    return go_path_exist


def docker_container_checks():
    container_exists = False
    outbuf = local("docker ps -a", capture=True)
    docker_ps = outbuf.split('\n')
    for container in docker_ps:
        container_name = container.split()[-1]
        if (container_name == GOBGP_CONTAINER_NAME) or \
                (container_name == EXABGP_CONTAINER_NAME) or ("q" in container_name):
            container_exists = True
    return container_exists


def docker_containers_get():
    containers = []
    cmd = "docker ps -a | awk '{print $NF}'"
    outbuf = local(cmd, capture=True)
    docker_ps = outbuf.split('\n')
    for container in docker_ps:
        if container != "NAMES":
            containers.append(container.split()[-1])
    return containers


def docker_container_set_ipaddress(bridge, quagga_name, address):
    cmd = "pipework " + bridge["BRIDGE_NAME"] + " -i eth-" + bridge["BRIDGE_NAME"]\
          + " " + quagga_name + " " + address
    local(cmd, capture=True)


def docker_container_run_quagga(quagga_num, bridge):
    quagga_name = "q" + str(quagga_num)
    cmd = "docker run --privileged=true -v " + CONFIG_DIR + "/" + quagga_name +\
          ":/etc/quagga --name " + quagga_name + " -id osrg/quagga"
    local(cmd, capture=True)
    aff_net = bridge["BRIDGE_NAME"][-1]
    quagga_address = "1" + aff_net + ".0.0." + str(quagga_num) + "/16"
    docker_container_set_ipaddress(bridge, quagga_name, quagga_address)


def docker_container_run_gobgp(bridge):
    cmd = "docker run --privileged=true -v " + CONFIG_DIR + ":/mnt -d --name "\
          + GOBGP_CONTAINER_NAME + " -id osrg/gobgp"
    local(cmd, capture=True)
    docker_container_set_ipaddress(bridge, GOBGP_CONTAINER_NAME, GOBGP_ADDRESS)


def docker_container_run_exabgp(bridge):
    pwd = local("pwd", capture=True)
    test_pattern_dir = pwd + "/exabgp_test_conf"
    cmd = "docker run --privileged=true -v " + test_pattern_dir + ":/etc/exabgp -v " \
          + CONFIG_DIR + ":/mnt -d --name " + EXABGP_CONTAINER_NAME + " -id osrg/exabgp"
    local(cmd, capture=True)
    docker_container_set_ipaddress(bridge, EXABGP_CONTAINER_NAME, EXABGP_ADDRESS)


def make_startup_file():
    file_buff = '#!/bin/bash' + '\n'
    file_buff += 'cd /go/src/github.com/osrg/gobgp' + '\n'
    file_buff += 'git pull origin master' + '\n'
    file_buff += 'go get -v' + '\n'
    file_buff += 'go build' + '\n'
    file_buff += './gobgp -f /mnt/gobgpd.conf > /mnt/gobgpd.log'
    cmd = "echo \"" + file_buff + "\" > " + CONFIG_DIRR + STARTUP_FILE_NAME
    local(cmd, capture=True)
    cmd = "chmod 755 " + CONFIG_DIRR + STARTUP_FILE_NAME
    local(cmd, capture=True)


def make_startup_file_use_local_gobgp():
    file_buff = '#!/bin/bash' + '\n'
    file_buff += 'rm -rf  /go/src/github.com/osrg/gobgp' + '\n'
    file_buff += 'cp -r /mnt/gobgp /go/src/github.com/osrg/' + '\n'
    file_buff += 'cd /go/src/github.com/osrg/gobgp' + '\n'
    file_buff += 'go get -v' + '\n'
    file_buff += 'go build' + '\n'
    file_buff += './gobgp -f /mnt/gobgpd.conf > /mnt/gobgpd.log'
    cmd = "echo \"" + file_buff + "\" > " + CONFIG_DIRR + STARTUP_FILE_NAME
    local(cmd, capture=True)
    cmd = "chmod 755 " + CONFIG_DIRR + STARTUP_FILE_NAME
    local(cmd, capture=True)


def docker_container_stop_quagga(quagga):
    cmd = "docker rm -f " + quagga
    local(cmd, capture=True)
    cmd = "rm -rf " + CONFIG_DIRR + quagga
    local(cmd, capture=True)


def docker_container_stop_gobgp():
    cmd = "docker rm -f " + GOBGP_CONTAINER_NAME
    local(cmd, capture=True)


def docker_container_stop_exabgp():
    cmd = "docker rm -f " + EXABGP_CONTAINER_NAME
    local(cmd, capture=True)


def docker_containers_destroy():
    containers = docker_containers_get()
    for container in containers:
        if re.match(r'q[0-9][0-9]*', container) is not None:
            docker_container_stop_quagga(container)
        if container == GOBGP_CONTAINER_NAME:
            docker_container_stop_gobgp()
        if container == EXABGP_CONTAINER_NAME:
            docker_container_stop_exabgp()
    bridge_unsetting_for_docker_connection()
    cmd = "rm -rf " + CONFIG_DIRRR
    local(cmd, capture=True)


def docker_container_quagga_append(quagga_num, bridge):
    print "start append docker container."
    docker_container_run_quagga(quagga_num, bridge)
    cmd = "docker exec gobgp /usr/bin/pkill gobgp -SIGHUP"
    local(cmd, capture=True)
    print "complete append docker container."


def docker_container_quagga_removed(quagga_num):
    print "start removed docker container."
    quagga = "q" + str(quagga_num)
    docker_container_stop_quagga(quagga)
    print "complete removed docker container."


def bridge_setting_for_docker_connection():
    bridge_unsetting_for_docker_connection()
    for bridge in BRIDGES:
        cmd = "brctl addbr " + bridge["BRIDGE_NAME"]
        local(cmd, capture=True)
        cmd = "ifconfig " + bridge["BRIDGE_NAME"] + " " + bridge["BRIDGE_ADDRESS"]
        local(cmd, capture=True)
        cmd = "ifconfig " + bridge["BRIDGE_NAME"] + " up"
        local(cmd, capture=True)


def bridge_unsetting_for_docker_connection():
    for bridge in BRIDGES:
        sysfs_name = "/sys/class/net/" + bridge["BRIDGE_NAME"]
        if os.path.exists(sysfs_name):
            cmd = "ifconfig " + bridge["BRIDGE_NAME"] + " down"
            local(cmd, capture=True)
            cmd = "brctl delbr " + bridge["BRIDGE_NAME"]
            local(cmd, capture=True)


def start_gobgp():
    cmd = "docker exec gobgp " + STARTUP_FILE + " > /dev/null 2>&1 &"
    local(cmd, capture=True)


def start_exabgp(conf_file):
    conf_path = EXABGP_CONFDIR + conf_file
    cmd = "docker exec exabgp /root/exabgp/sbin/exabgp " + conf_path + " > /dev/null 2>&1 &"
    local(cmd, capture=True)


def get_notification_from_exabgp_log():
    log_path = CONFIG_DIRR + EXABGP_LOG_FILE
    cmd = "grep notification " + log_path + " | head -1"
    err_mgs = local(cmd, capture=True)
    return err_mgs


def make_config(quagga_num, go_path):
    if go_path != "":
        print "specified go path is [ " + go_path + " ]."
        if os.path.isdir(go_path):
            go_path += "/"
        else:
            print "specified go path do not use."
    pwd = local("pwd", capture=True)
    cmd = go_path + "go run " + pwd + "/quagga-rsconfig.go -n " + str(quagga_num) + " -c /usr/local/gobgp"
    local(cmd, capture=True)


def make_config_append(quagga_num, go_path):
    if go_path != "":
        print "specified go path is [ " + go_path + " ]."
        if os.path.isdir(go_path):
            go_path += "/"
        else:
            print "specified go path do not use."
    pwd = local("pwd", capture=True)
    cmd = go_path + "go run " + pwd + "/quagga-rsconfig.go -a " + str(quagga_num) + " -c /usr/local/gobgp"
    local(cmd, capture=True)


def init_test_env_executor(quagga_num, use_local, go_path):
    print "start initialization of test environment."

    if docker_container_checks():
        print "gobgp test environment already exists."
        print "so that remake gobgp test environment."
        docker_containers_destroy()

    print "make gobgp test environment."
    bridge_setting_for_docker_connection()
    make_config(quagga_num, go_path)

    # run each docker container
    for num in range(1, quagga_num + 1):
        docker_container_run_quagga(num, BRIDGE_0)
    docker_container_run_gobgp(BRIDGE_0)

    # execute local gobgp program in the docker container if the input option is local
    if use_local:
        print "execute gobgp program in local machine."
        pwd = local("pwd", capture=True)
        if A_PART_OF_CURRENT_DIR in pwd:
            gobgp_path = re.sub(A_PART_OF_CURRENT_DIR, "", pwd)
            cmd = "cp -r " + gobgp_path + " " + CONFIG_DIRR
            local(cmd, capture=True)
            make_startup_file_use_local_gobgp()
        else:
            print "scenario_test directory is not."
            print "execute gobgp program of osrg/master in github."
            make_startup_file()
    else:
        print "execute gobgp program of osrg/master in github."
        make_startup_file()

    start_gobgp()

    print "complete initialization of test environment."


def init_malformed_test_env_executor(conf_file, use_local):
    print "start initialization of exabgp test environment."
    if docker_container_checks():
        print "gobgp test environment already exists."
        print "so that remake gobgp test environment."
        docker_containers_destroy()

    print "make gobgp test environment."
    bridge_setting_for_docker_connection()
    pwd = local("pwd", capture=True)
    gobgp_file = pwd + "/exabgp_test_conf/gobgpd.conf"
    cmd = "cp " + gobgp_file + " " + CONFIG_DIRR
    local(cmd, capture=True)
    quagga_dir = CONFIG_DIRR + "q1"
    cmd = "mkdir " + quagga_dir
    local(cmd, capture=True)
    quagga_file = pwd + "/exabgp_test_conf/quagga.conf"
    cmd = "cp " + quagga_file + " " + quagga_dir + "/bgpd.conf"
    local(cmd, capture=True)
    docker_container_run_quagga(1, BRIDGE_0)
    docker_container_run_gobgp(BRIDGE_0)
    docker_container_run_exabgp(BRIDGE_0)

    # execute local gobgp program in the docker container if the input option is local
    if use_local:
        print "execute gobgp program in local machine."
        pwd = local("pwd", capture=True)
        if A_PART_OF_CURRENT_DIR in pwd:
            gobgp_path = re.sub(A_PART_OF_CURRENT_DIR, "", pwd)
            cmd = "cp -r " + gobgp_path + " " + CONFIG_DIRR
            local(cmd, capture=True)
            make_startup_file_use_local_gobgp()
        else:
            print "scenario_test directory is not."
            print "execute gobgp program of osrg/master in github."
            make_startup_file()

    else:
        print "execute gobgp program of osrg/master in github."
        make_startup_file()
        
    start_gobgp()
    start_exabgp(conf_file)


def docker_container_quagga_append_executor(quagga_num, go_path):
    make_config_append(quagga_num, go_path)
    docker_container_quagga_append(quagga_num, BRIDGE_0)


def docker_container_quagga_removed_executor(quagga_num):
    docker_container_quagga_removed(quagga_num)


def docker_container_make_bestpath_env_executor(append_quagga_num, go_path):
    print "start make bestpath environment"
    make_config_append(append_quagga_num, go_path)
    append_quagga_name = "q" + str(append_quagga_num)
    docker_container_quagga_append(append_quagga_num, BRIDGE_1)
    docker_container_set_ipaddress(BRIDGE_1, "q2", "11.0.0.2/16")
    docker_container_set_ipaddress(BRIDGE_2, append_quagga_name, "12.0.0.20/16")
    docker_container_set_ipaddress(BRIDGE_2, "q3", "12.0.0.3/16")
