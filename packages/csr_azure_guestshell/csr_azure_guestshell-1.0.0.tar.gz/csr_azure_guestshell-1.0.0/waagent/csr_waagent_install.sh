#!/bin/bash

echo "Installing waagent" >> /home/guestshell/azure/azure_env.log
cd waagent
echo "going to install rpm" >> /home/guestshell/azure/azure_env.log
yum -y localinstall WALinuxAgent-2.2.14.1.4-1.noarch.rpm
echo "Starting waagent daemon" >> /home/guestshell/azure/azure_env.log
service waagent start
systemctl status waagent >> /home/guestshell/azure/azure_env.log
echo "Waagent daemon running" >> /home/guestshell/azure/azure_env.log
