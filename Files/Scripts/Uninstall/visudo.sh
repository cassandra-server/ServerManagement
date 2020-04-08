#!/bin/bash
line="$USER ALL = NOPASSWD: $HOME/.ServerManagement/Files/Scripts/Uninstall/daemon.sh" 
sed -i "/$line/d" /etc/sudoers.tmp
line="$USER ALL = NOPASSWD: $HOME/.ServerManagement/Files/Scripts/Uninstall/visudo.sh"
sed -i "/$line/d" /etc/sudoers.tmp
