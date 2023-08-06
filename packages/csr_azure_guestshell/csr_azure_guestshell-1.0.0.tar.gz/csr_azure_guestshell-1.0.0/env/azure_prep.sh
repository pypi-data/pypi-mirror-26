#!/bin/sh

# Set up the environment for supporting Azure in the guestshell
#
# This script assumes the guestshell has been configured and enabled on
# the CSR.

env_log="/home/guestshell/azure/azure_env.log"

# Set up a directory tree for Azure stuff
if [ ! -d /home/guestshell/azure ]; then
    mkdir /home/guestshell/azure
    chmod 777 azure
    cd bin
    cp * /home/guestshell/azure
    cd ../examples
    cp * /home/guestshell/azure
    cd ../env
    cp * /home/guestshell/azure
    cd ../csr_azure_guestshell
    cp * /home/guestshell/azure
fi

echo "Set up Azure environment" > $env_log

