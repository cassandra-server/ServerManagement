#!/bin/bash
ssh -t -p `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverport.txt` `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` sudo transmission-remote -a `cat $HOME/.ServerManagement/Files/Resources/Args/magnetlink.txt`
