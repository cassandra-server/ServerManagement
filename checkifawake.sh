if ! ping -q -w3 -c 1 your_ip_address >/dev/null #make a ping for 3 seconds to the desired ip and wait for an answer
	then
		echo "asleep" >path_to_file/status.txt #if there's no answer type asleep on status.txt
else
		echo "awake" >path_to_file/status.txt #if there's an answer type awake on status.txt
fi
