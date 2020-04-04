#!/bin/bash
mkdir $HOME/.ServerManagement
wget https://github.com/MiguelSanchezP/ServerManagement/archive/master.zip -P $HOME/.ServerManagement/
unzip $HOME/.ServerManagement/master.zip -d $HOME/.ServerManagement/ && mv $HOME/.ServerManagement/ServerManagement-master/* $HOME/.ServerManagement/ && rm -r $HOME/.ServerManagement/ServerManagement-master/
rm $HOME/.ServerManagement/master.zip
read -p "What is the Telegram Bot Token: " token
echo $token > $HOME/.ServerManagement/Files/Resources/Authentication/Functioning/token.txt
read -p "Write the userId of the superuser: " userid
echo $userid > $HOME/.ServerManagement/Files/Resources/Authentication/Functioning/superuserIds.txt
echo $userid > $HOME/.ServerManagement/Files/Resources/Authentication/Functioning/userIds.txt
read -p "Write the name to recognize the server: " servername
read -p "Write the username to access the machine: " serveruser
read -p "Write the ip address of the server: " serverip
read -p "Write the mac address of the server: " servermac
echo $serveruser > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt
echo $serverip > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt
echo $servermac > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/servermac.txt
echo "$servername $serveruser $serverip $servermac" > $HOME/.ServerManagement/Files/Resources/Authentication/Machines/machines.txt
