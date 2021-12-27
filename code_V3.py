import os
import subprocess
import re
import sys
import concurrent.futures

def ping(host):
    ping_out = ''
    command = 'ping -c 5 ' + ip
    response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    #print(response.stdout)
    ping_out = ping_out + '\n' + response.stdout + '\n'
    return ping_out

def trace(host, proto, port):
    trace_out = ''
    if proto == 'tcp':
        command = 'traceroute -T -p ' + str(port) + ' ' + str(ip) + ' -nn'
    else:
        command = 'traceroute -p ' + str(port) + ' ' + str(ip) + ' -nn'
    response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    #print(response.stdout)
    trace_out = trace_out + '\n' + response.stdout + '\n'
    return trace_out

def mtr(host, proto, port):
    mtr_out = ''
    if proto == 'tcp':
        command = 'mtr -T -n -P ' + str(port)  + ' ' +  str(ip) + ' --report'
    else:
        command = 'mtr --udp -n -P ' + str(port)  + ' ' +  str(ip) + ' --report'
    response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    #print(response.stdout)
    mtr_out = mtr_out + '\n' + response.stdout + '\n'
    return mtr_out

def hping(host, proto, port):
    hping_out = ''
    if proto == 'tcp':
        command = 'hping3 -S -p ' + str(port) + ' -c 10 ' + str(ip)
    else:
        command = 'hping3 --udp -p ' + str(port) + ' -c 10 ' + str(ip)
    response = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    #print(response.stdout)
    hping_out = hping_out + '\n' + response.stdout + '\n' + response.stderr + '\n'
    return hping_out


for i in range(int(len(sys.argv))):
    if sys.argv[i] == '--help':
        print(f'Syntax for the usage of the script is ./<file.py> <ip-address> <protocol tcp/udp> <port_number> ')
        sys.exit()

if len(sys.argv) == int(0):
    print(f'You did not pass any argumets. Please specify the argumets for the script')
    sys.exit()
elif len(sys.argv) > int(4):
    print(f'Please specify all argumets for the script. check --help for more details. ')
    sys.exit()
else:
    ip = sys.argv[1]
    protocol = sys.argv[2]
    port = sys.argv[3]

    # create output files
    directory = os.getcwd()
    regex = re.compile("/.*")
    ping_file = 'ping_result'
    a = subprocess.run(f'touch {str(directory)}/{str(ping_file)}.text', shell=True, universal_newlines=True)
    ping_file = regex.search(a.args)

    traceroute_file = 'trace_result'
    b = subprocess.run(f'touch {str(directory)}/{str(traceroute_file)}.text', shell=True, universal_newlines=True)
    traceroute_file = regex.search(b.args)

    mtr_file = 'mtr_result'
    c = subprocess.run(f'touch {str(directory)}/{str(mtr_file)}.text', shell=True, universal_newlines=True)
    mtr_file = regex.search(c.args)

    hping_file = 'hping_result'
    c = subprocess.run(f'touch {str(directory)}/{str(hping_file)}.text', shell=True, universal_newlines=True)
    hping_file = regex.search(c.args)

    # check date from system
    date = subprocess.run('date', shell=True, universal_newlines=True, stdout=subprocess.PIPE)
    date = date.stdout

    # multiple-thread so that the commands does not wait for the other commands to finish
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ping_out = []
        trace_out = []
        mtr_out = []
        hping_out = []

        ping_out.append(executor.submit(ping, ip))
        trace_out.append(executor.submit(trace, ip, protocol, port))
        mtr_out.append(executor.submit(mtr, ip, protocol, port))
        hping_out.append(executor.submit(hping, ip, protocol, port))


        for p in concurrent.futures.as_completed(ping_out):
            with open(ping_file.group(0), 'a') as ping_result:
                ping_result.write(date)
                ping_result.write(p.result())

        for t in concurrent.futures.as_completed(trace_out):
            with open(traceroute_file.group(0), 'a') as trace_result:
                trace_result.write(date)
                trace_result.write(t.result())

        for m in concurrent.futures.as_completed(mtr_out):
            with open(mtr_file.group(0), 'a') as mtr_result:
                mtr_result.write(date)
                mtr_result.write(m.result())

        for h in concurrent.futures.as_completed(hping_out):
            with open(hping_file.group(0), 'a') as hping_result:
                hping_result.write(date)
                hping_result.write(h.result())

    print(f'check output in following files \n {ping_file.group(0)} \n {traceroute_file.group(0)} \n {mtr_file.group(0)} \n {hping_file.group(0)}')
