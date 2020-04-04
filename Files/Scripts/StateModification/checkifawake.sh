#!/bin/bash
if ! ping -q -w3 -c 1 `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` #ping the desired ip during 3 seconds to know the status (change to your own IP or domain)
	then
		echo "asleep" > $HOME/.ServerManagement/Files/Resources/Outputs/status.txt #write output in status.txt (change path to your own)
else
		echo "awake" > $HOME/.ServerManagement/Files/Resources/Outputs/status.txt #write output to status.txt (change path to your own)
fi
