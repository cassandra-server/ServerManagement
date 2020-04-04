#!/bin/bash
wakeonlan `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/servermac.txt` ; while ! ping -q -c 1 `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` ; do sleep 1 ; done #turn on and ping until positive response (put your own mac and ip adress)
