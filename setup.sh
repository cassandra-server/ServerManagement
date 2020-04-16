#!/bin/bash
mkdir $HOME/.ServerManagement
wget https://github.com/MiguelSanchezP/ServerManagement/archive/master.zip -P $HOME/.ServerManagement/
unzip $HOME/.ServerManagement/master.zip -d $HOME/.ServerManagement/ && mv $HOME/.ServerManagement/ServerManagement-master/* $HOME/.ServerManagement/ && rm -r $HOME/.ServerManagement/ServerManagement-master/
rm $HOME/.ServerManagement/master.zip
apt install python3 python3-pip
pip3 install python-telegram-bot
read -p "What is the Telegram Bot Token: " token
echo $token > $HOME/.ServerManagement/Files/Resources/Authentication/Functioning/token.txt
read -p "Write the userId of the superuser (access to all functions): " userid
echo $userid > $HOME/.ServerManagement/Files/Resources/Authentication/Functioning/superuserIds.txt
echo $userid > $HOME/.ServerManagement/Files/Resources/Authentication/Functioning/userIds.txt
read -p "Write the name to recognize the server: " servername
read -p "Write the username to access the machine: " serveruser
read -p "Write the ip address of the server: " serverip
read -p "Write the mac address of the server: " servermac
read -p "Write the OpenSSH port of the server (default=22): " serverport
if [-z "$serverport"]; then
	$serverport=22
fi
echo $serveruser > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt
echo $serverip > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt
echo $servermac > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/servermac.txt
echo $serverport > $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverport.txt
echo "$servername $serveruser $serverip $servermac $serverport $userid" > $HOME/.ServerManagement/Files/Resources/Authentication/Machines/machines.txt
chmod -R +x $HOME/.ServerManagement/Files/Scripts/
touch /lib/systemd/system/bot.service
echo "[Unit]" > /lib/systemd/system/bot.service
echo "Description=A Telegram bot that is capable of controlling many aspects of servers on the same network" >> /lib/systemd/system/bot.service
echo "After=multi-user.target" >> /lib/systemd/system/bot.service
echo "" >> /lib/systemd/system/bot.service
echo "[Service]" >> /lib/systemd/system/bot.service
echo "User=$USER" >> /lib/systemd/system/bot.service
echo "Type=idle" >> /lib/systemd/system/bot.service
echo "ExecStart=/usr/bin/python3 $HOME/.ServerManagement/ServerManagement.py" >> /lib/systemd/system/bot.service
echo "" >> /lib/systemd/system/bot.service
echo "[Install]" >> /lib/systemd/system/bot.service
echo "WantedBy=multi-user.target" >> /lib/systemd/system/bot.service
systemctl daemon-reload
systemctl enable bot.service
systemctl start bot.service
echo "$USER ALL = NOPASSWD: $HOME/.ServerManagement/Files/Scripts/Uninstall/daemon.sh" >> /etc/sudoers.tmp
echo "$USER ALL = NOPASSWD: $HOME/.ServerManagement/Files/Scripts/Uninstall/visudo.sh" >> /etc/sudoers.tmp
