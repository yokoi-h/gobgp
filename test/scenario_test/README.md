Route Server Scenario Test
========================

Preparation
-----------
Please set up Ubuntu 14.04 Server Edition virtual machine,
and install golang environment inside the VM.

Setup
-----
Execute the following commands inside the VM:

- ##### 1. Install and setting the packages required to run the scenario test.
```shell
$ sudo apt-get update
$ sudo apt-get install git python-pip python-dev iputils-arping bridge-utils lv
$ sudo wget https://raw.github.com/jpetazzo/pipework/master/pipework -O /usr/local/bin/pipework
$ sudo chmod 755 /usr/local/bin/pipework
$ sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
$ sudo apt-get install docker-engine
$ gpasswd -a `whoami` docker
```


- ##### 2. Get each docker image from Docker Hub.
```shell
$ sudo docker pull osrg/golang:1.5
$ sudo docker pull osrg/quagga
$ sudo docker pull osrg/gobgp
```

- ##### 3. Download gobgp and install python libraries.
```shell
$ git clone https://github.com/osrg/gobgp.git
$ cd ./gobgp
$ GOBGP_DIR=`pwd`
$ cd ${GOBGP_DIR}/test/scenario_test
$ pip install -r pip-requires.txt
```


Start
-----
Please run the test script as root.

```shell
bgp_router_test.py
bgp_zebra_test.py
evpn_test.py
flow_spec_test.py
global_policy_test.py
ibgp_router_test.py
route_reflector_test.py
route_server_ipv4_v6_test.py
route_server_policy_grpc_test.py
route_server_policy_test.py
route_server_test.py

run_all_tests.sh
```

 * route_server_test.py is scenario test script.

```
# python route_server_test.py -v [ --use-local ] [--go-path=<path>]

```


 * If you want to do malformed packet test, please run route_server_malformed_test.py

```
# python route_server_malformed_test.py -v [ --use-local ] [ --go-path=<path> ]

```

- If you want to do scenario test in ipv4 and ipv6 mixed environment, please run route_server_ipv4_v6_test.py

```
# python route_server_ipv4_v6_test.py -v [ --use-local ] [ --go-path=<path> ]

```


After the test, test results will be shown.

Options
-----
 use [ --use-local ] option when execute gobgp program of local system.

 use [ --go-path ] option when not root and use sudo command.


Examples
-----
 How to use [ --use-local ] option
```
# python route_server_test.py -v --use-local
```

 How to use [ --go-path=<path> ] option
```
$ sudo -E python route_server_test.py -v --go-path=/usr/local/go/bin
```