ssh -t `cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serveruser.txt`@`cat $HOME/.ServerManagement/Files/Resources/Authentication/SSH/serverip.txt` sudo transmission-remote -a `cat $HOME/.ServerManagement/Files/Scripts/SSH/magnetlink.txt`
