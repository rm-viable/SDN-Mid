from netmiko import ConnectHandler
import re

def leased_ip_check():
    
    ios_r1 = {
    'device_type':'cisco_ios',
    'username':'lab',
    'password':'lab123',
    'ip':'192.168.100.1',
    }

    conn = ConnectHandler(**ios_r1)
    output = conn.send_command("sh ip dhcp binding")
    reg = r'192.168.100.\d+'
    match = re.findall(reg,output)
    ip_leased = match[0]
    return ip_leased
    
check = leased_ip_check()
print('********* The IP leased to Mininet VM is: ' + check)