import time
import os
from flask import Flask,render_template
from netmiko import ConnectHandler
import matplotlib
import re
from matplotlib import pyplot as p
import io
import base64
matplotlib.use('Agg')

mininet={
'device_type':'linux',
'username':'mininet',
'password':'mininet',
'ip':'192.168.100.2',
}

app=Flask(__name__)

global conn,y
#y values of the plot, the packet in counters
y=[]
#x values, time in seconds
x=[0]
conn=ConnectHandler(**mininet)

@app.route('/')
def index():

    y_length = len(y)
    
    #searching for packet in messages from switch to controller
    conn.write_channel("echo mininet | sudo -S ovs-ofctl dump-flows s1 --protocols=OpenFlow13 | grep 'priority=0 actions=CONTROLLER:65535'\n")
    time.sleep(1)
    output = conn.read_channel()
    #print(output)
    if "word" in output:
        conn.write_channel("mininet\n")
        time.sleep(1)    

    #searching for n_packets in the dump-flows output    
    reg = r'(?m)(?<=\bn_packets=)\d+'
    match = re.findall(reg,output)
    if len(y)>0:
        temp = int(match[0])- sum(y)
        x.append(y_length*5)
    else:
        temp = int(match[0])
        
    y.append(temp)
    y_length += 1
    
    #plot graph
    p.plot(x,y)
    p.title("OpenFlow Packet_In Montitor")
    p.xlabel("Time(s)")
    p.ylabel("Packet_In count")

    #parse graph to flask
    bitholder = []
    img_src = io.BytesIO()
    p.savefig(img_src,format='png')
    img_src.seek(0)
    base_url = base64.b64encode(img_src.getvalue()).decode()
    p.close()
    bitholder.append('data:image/png;base64,{}'.format(base_url))
    
    return render_template('pkt_in_gui.html',my_image = bitholder[0])

if __name__=="__main__":
    print("Capturing Packet_IN messages")
    app.run(debug=True)
