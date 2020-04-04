#!/bin/bash
ssh -t `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` find ~/`cat $HOME/.ServerManagement/Files/Resources/Args/dir.txt` > $HOME/.ServerManagement/Files/Resources/Outputs/list.txt
