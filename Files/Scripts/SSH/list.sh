#!/bin/bash
ssh -t -p `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverport.txt` `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` ls -1 ~/`cat $HOME/.ServerManagement/Files/Resources/Args/dir.txt` > $HOME/.ServerManagement/Files/Resources/Outputs/list.txt
