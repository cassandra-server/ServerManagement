if ! ping -q -w3 -c 1 ip_address #ping the desired ip during 3 seconds to know the status (change to your own IP or domain)
	then
		echo "asleep" > absolute_path/Files/Resources/Outputs/status.txt #write output in status.txt (change path to your own)
else
		echo "awake" > absolute_path/Files/Resources/Outputs/status.txt #write output to status.txt (change path to your own)
fi
