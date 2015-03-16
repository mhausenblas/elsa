#!/bin/bash

###############################################################################
# Provisioning script for deploying ElSA on Ubuntu 14.04 with Playa Mesos
#
# Usage: called via Vagrant shell provisioner
#
# Author: Michael Hausenblas
# Init: 2015-03-16


set -e # exit on error immediately, just to keep things sane


###############################################################################
# Global variables

SCRIPT_PATH=`dirname $0`

BASE_INSTALL=/home/vagrant

SPARK_CONF_TEMPLATE=$(cat <<EOF
export MESOS_NATIVE_LIBRARY=/usr/local/lib/libmesos.so
export SPARK_EXECUTOR_URI=file://$BASE_INSTALL/spark-1.2.0/spark-1.2.0.tgz
export MASTER=mesos://127.0.1.1:5050
EOF
)

pushd $BASE_INSTALL # remember where we started and change into install dir

echo Provisioning ElSA into $BASE_INSTALL

###############################################################################
# Base: Marathon Python lib and Spark
#
#  - marathon-python https://github.com/thefactory/marathon-python
#  - Apache Spark 1.2.x https://spark.apache.org/downloads.html

echo Phase 1: Marathon Python lib and Spark

sudo apt-get -y update

# Install marathon-python
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py
pip install marathon

# Install and configure JDK (for Spark and ElSA)
sudo apt-get -y install default-jdk
export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:bin/javac::")

# Install and configure Maven (for Spark and ElSA)
sudo apt-get -y install maven
export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512M -XX:ReservedCodeCacheSize=512m"


###############################################################################
# Building Spark
#

echo Phase 2: Building Spark

cd $BASE_INSTALL # just to make sure

# Download Spark source files
wget http://d3kbcqa49mib13.cloudfront.net/spark-1.2.0.tgz
tar xzf spark-1.2.0.tgz && cd spark-1.2.0/

# Build Spark using Maven
mvn -DskipTests clean package
./make-distribution.sh
mv dist spark-1.2.0
tar czf spark-1.2.0.tgz spark-1.2.0/

# Configure Spark to use Mesos
cd conf/
cp spark-env.sh.template spark-env.sh
echo $SPARK_CONF_TEMPLATE >> spark-env.sh


###############################################################################
# Building ElSA

echo Phase 3: Building ElSA

cd $BASE_INSTALL # back to the base install dir to set up ElSA
git clone https://github.com/mhausenblas/elsa.git
cd elsa
mvn clean package

echo Done provisioning ElSA into $BASE_INSTALL

popd # restore and change back to where we started

exit 0