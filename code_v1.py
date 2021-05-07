import os
import subprocess
import re

def ping(host):
    ping_out = ''
    for ip in host:
        command = 'ping -c 5 ' + str(ip)
        response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        #print(response.stdout)
        ping_out = ping_out + '\n' + response.stdout
    return ping_out

def trace(host, proto, port):
    trace_out = ''
    for ip in host:
        if proto == 'tcp':
            command = 'traceroute -T -p ' + str(port) + ' ' + str(ip) + ' -nn'
        else:
            command = 'traceroute -p ' + str(port) + ' ' + str(ip) + ' -nn'
        response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        #print(response.stdout)
        trace_out = trace_out + '\n' + response.stdout
    return trace_out

def mtr(host, proto, port):
    mtr_out = ''
    for ip in host:
        if proto == 'tcp':
            command = 'mtr -T -P ' + str(port)  + ' ' +  str(ip) + ' --report'
        else:
            command = 'mtr --udp -P ' + str(port)  + ' ' +  str(ip) + ' --report'
        response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
        #print(response.stdout)
        mtr_out = mtr_out + '\n' + response.stdout
    return mtr_out

ip_list = []
# get the ip list from user
number_of_ip = input('Please specify the number of IP, you want to monitor ')
for i in range(int(number_of_ip)):
    ip_list.append(input('Please specify ' + str(i + 1) + ' IP : '))
print(f'IP you have entered are {ip_list}')

# get the port and protocol from user
protocol = input('Please specify the protocol(tcp or udp) you want to use :' )
port = input('Please specify the port you would like to monitor :')

# create output files
directory = os.getcwd()
regex = re.compile("/.*")
ping_file = input('Please specify the name of the ping output file : ')
a = subprocess.run(f'touch {str(directory)}/{str(ping_file)}.text', shell=True, universal_newlines=True)
ping_file = regex.search(a.args)
#p_file = ping_file(0)

traceroute_file = input('Please specify the name of the traceroute output file : ')
b = subprocess.run(f'touch {str(directory)}/{str(traceroute_file)}.text', shell=True, universal_newlines=True)
traceroute_file = regex.search(b.args)
#t_file = traceroute_file(0)

mtr_file = input('Please specify the name of the MTR output file : ')
c = subprocess.run(f'touch {str(directory)}/{str(mtr_file)}.text', shell=True, universal_newlines=True)
mtr_file = regex.search(c.args)
#m_file = mtr_file(0)

# check date from system
date = subprocess.run('date', shell=True, universal_newlines=True, stdout=subprocess.PIPE)
date = date.stdout

ping_out = ping(ip_list)
with open(ping_file.group(0), 'a') as ping_result:
    ping_result.write(date)
    ping_result.write(ping_out)

trace_out = trace(ip_list, protocol, port)
with open(traceroute_file.group(0), 'a') as trace_result:
    trace_result.write(date)
    trace_result.write(trace_out)

mtr_out = mtr(ip_list, protocol, port)
with open(mtr_file.group(0), 'a') as mtr_result:
    mtr_result.write(date)
    mtr_result.write(mtr_out)

print(f'check output in following files \n {ping_file.group(0)} \n {traceroute_file.group(0)} \n {mtr_file.group(0)}')
