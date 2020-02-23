if ! ping -q -w3 -c 1 put_your_ip_here >/dev/null #ping the desired ip during 3 seconds to know the status (change to your own IP or domain)
	then
		echo "asleep" >path_to_the_folder/resources/status.txt #write output in status.txt (change path to your own)
else
		echo "awake" >path_to_the_folder/resources/status.txt #write output to status.txt (change path to your own)
fi
