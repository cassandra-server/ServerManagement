#!/bin/bash
ssh -t -p `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverport.txt` `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` "sudo mv /var/lib/transmission-daemon/downloads/* ~/Films/Unformatted/"
