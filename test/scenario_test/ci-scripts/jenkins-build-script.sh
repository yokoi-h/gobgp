# renew GOPATH
rm -rf /usr/local/jenkins/{bin,pkg,src}
mkdir /usr/local/jenkins/{bin,pkg,src}
mkdir -p /usr/local/jenkins/src/github.com/osrg/

export GOBGP_IMAGE=gobgp
export GOPATH=/usr/local/jenkins
export GOROOT=/usr/local/go
export GOBGP=/usr/local/jenkins/src/github.com/osrg/gobgp
export WS=`pwd`

rm -r ${WS}/nosetest*.xml
cp -r ../workspace $GOBGP
pwd
cd $GOBGP
ls -al
git log | head -20

sudo docker rmi $(sudo docker images | grep "^<none>" | awk '{print $3}')
sudo docker rm -f $(sudo docker ps -a -q)

for link in $(ip li | awk '/(_br|veth)/{sub(":","", $2); print $2}')
do
    sudo ip li set down $link
    sudo ip li del $link
done

sudo fab -f $GOBGP/test/scenario_test/lib/base.py make_gobgp_ctn --set tag=$GOBGP_IMAGE

cd $GOBGP/gobgpd
$GOROOT/bin/go get -v

cd $GOBGP/test/scenario_test

sudo rm /var/log/upstart/docker.log
sudo touch /var/log/upstart/docker.log
./run_all_tests.sh

mkdir ${WS}/jenkins-log-${BUILD_NUMBER}
sudo cp ${WS}/*.xml ${WS}/jenkins-log-${BUILD_NUMBER}/
sudo cp /var/log/upstart/docker.log ${WS}/jenkins-log-${BUILD_NUMBER}/docker.log
sudo chown -R jenkins:jenkins ${WS}/jenkins-log-${BUILD_NUMBER}

tar cvzf ${WS}/jenkins-log-${BUILD_NUMBER}.tar.gz ${WS}/jenkins-log-${BUILD_NUMBER}
s3cmd put ${WS}/jenkins-log-${BUILD_NUMBER}.tar.gz s3://gobgp/jenkins/
rm -rf ${WS}/jenkins-log-${BUILD_NUMBER} ${WS}/jenkins-log-${BUILD_NUMBER}.tar.gz
