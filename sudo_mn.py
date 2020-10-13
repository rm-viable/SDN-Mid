import leased_ip
from netmiko import ConnectHandler
import time
import re

def sudo_mn(ip):
    
    mininet={
    'device_type':'linux',
    'username':'mininet',
    'password':'mininet',
    'ip':ip,
    }
    
    #connect to mininet vm
    conn=ConnectHandler(**mininet)
    
    #starting up default mininet topology
    conn.write_channel("echo mininet | sudo -S mn\n")
    time.sleep(1)
    output = conn.read_channel()
    print(output)

lsd_ip = leased_ip.leased_ip_check()

sudo_mn(lsd_ip)