ssh -t username@ip_address pidof sftp-server | tee path_to_files/resources/mountedServers.txt #replace with your own paths and ip's (assuming the server is mounted on sshfs)
