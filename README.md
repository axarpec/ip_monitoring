# ip_monitoring
ip_monitoring from liunx

V1 :
- This script can take input from users in terms of IP that users wants to monitor.
- This script can check the connectivity with specific protocol and specific port.
- This script will create log file under the current working directory.

V2 :
- This script can take input from the users in terms of the time duration in which user wants to run test.
- This script can pull the ping/traceroute/mtr result at the specific interval defined by user.
- This script is making use of multithreading in order to speedup the process.

V3 :
- This script is to make it compatible with the linux cronjob setup where one can pass arguments with the script and start monitoring the IP.
- The interval that the script will run can be managed by the cronjob.

Note : For v3 to run in the linux env, I would recommend to put the sheband as following and make the script executable with chmod.
#!/usr/bin/env python3

Stay tuned for more updates.
