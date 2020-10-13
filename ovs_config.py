import leased_ip
from netmiko import ConnectHandler
import time
import re

def ovs_config(ip):
    
    mininet={
    'device_type':'linux',
    'username':'mininet',
    'password':'mininet',
    'ip':ip,
    }
    
    conn=ConnectHandler(**mininet)
    
    #adding route default through eth0 in order for mininet vm to be able to connect to controller
    #delete if route exists
    conn.write_channel("echo mininet | sudo -S ip route del 0.0.0.0/0\n")
    time.sleep(1)
    #add it back
    conn.write_channel("echo mininet | sudo -S ip route add 0.0.0.0/0 dev eth0\n")
    time.sleep(1)
    
    #starting up default mininet topology
    conn.write_channel("sudo mn\n")
    time.sleep(1)
    output = conn.read_channel()
    print(output)
    if "word" in output:
        conn.write_channel("mininet\n")
        time.sleep(2)   
    
    #set openflow version
    conn.write_channel("sh ovs-vsctl set bridge s1 protocols=OpenFlow13\n")
    time.sleep(2)
    print("\n")
    print("******** OpenFlow version --> 1.3\n")
    
    #set controller ip address and port number
    conn.write_channel("sh ovs-vsctl set-controller s1 tcp:10.20.30.2:6653\n")
    time.sleep(5)
    print("******** Controller configured!")

lsd_ip = leased_ip.leased_ip_check()

ovs_config(lsd_ip)