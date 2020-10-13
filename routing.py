from netmiko import ConnectHandler
import time

def routing():
    ios_r1={
    'device_type':'cisco_ios',
    'username':'lab',
    'password':'lab123',
    'ip':'192.168.100.1',
    }
    
    ios_r2={
    'device_type':'cisco_ios',
    'username':'lab',
    'password':'lab123',
    'ip':'192.168.200.2',
    }
    
    ios_r4={
    'device_type':'cisco_ios',
    'username':'lab',
    'password':'lab123',
    'ip':'172.16.100.1',
    }

    net_connect1=ConnectHandler(**ios_r1)
    output = net_connect1.send_config_set(["router ospf 1","network 0.0.0.0 255.255.255.255 area 0"])
    print(output)
    print('\n')
    print('********* Routing enabled on: ios_r1')


    net_connect1.write_channel("ssh -l lab 192.168.200.2\n")
    time.sleep(1)
    output2 = net_connect1.read_channel()
    if "word" in output2:
        net_connect1.write_channel(net_connect1.password + '\n')
    time.sleep(1)

    
    net_connect1.write_channel("conf t\n")
    net_connect1.write_channel("router ospf 1\n")
    net_connect1.write_channel("network 0.0.0.0 255.255.255.255 area 0\n")
    net_connect1.write_channel("end\n")
    print('\n')
    print('********* Routing enabled on: ios_r2')
    time.sleep(4)

        
    net_connect1.write_channel("ssh -l lab 172.16.100.1\n")
    time.sleep(4)
    output3 = net_connect1.read_channel()
    if "word" in output3:
        net_connect1.write_channel(net_connect1.password + '\n')
    net_connect1.write_channel("conf t\n")
    net_connect1.write_channel("router ospf 1\n")
    net_connect1.write_channel("network 0.0.0.0 255.255.255.255 area 0\n")
    net_connect1.write_channel("end\n")
    print('\n')
    print('********* Routing enabled on: ios_r4')

routing()