#!/bin/bash
ssh -t `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` "sudo reboot" ; sleep 10 ; while ! ping -q -c 1 `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` ; do sleep 1 ; done
