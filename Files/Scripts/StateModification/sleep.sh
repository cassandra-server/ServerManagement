#!/bin/bash
ssh -t -p `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverport.txt` `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` "sudo shutdown -P 0" #send the command to shutdown to the server (put your own username and ip)
