import time
import os
from flask import Flask,render_template
from netmiko import ConnectHandler
import matplotlib
import re
from matplotlib import pyplot as p
from matplotlib import pyplot as p1
from matplotlib import pyplot as p2
from matplotlib import pyplot as p3
from matplotlib import pyplot as p4
from matplotlib import pyplot as p5
import io
import base64
import smtplib
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

#y values of the plot, the packet in counters
y1=[]
#x values, time in seconds
x1=[0]

#y values of the plot, the packet in counters
y2=[]
#x values, time in seconds
x2=[0]

#y values of the plot, the packet in counters
y3=[]
#x values, time in seconds
x3=[0]

#y values of the plot, the packet in counters
y4=[]
#x values, time in seconds
x4=[0]

#y values of the plot, the packet in counters
y5=[]
#x values, time in seconds
x5=[0]


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
    print('Number of Packet_INs to controller in this iteration is: {}'.format(match[0]))
    if len(y)>0:
        temp = int(match[0])
        x.append(y_length*5)
    else:
        temp = int(match[0])
        
    y.append(temp)
    
    y_length += 1

    y1_length = len(y1)
    
    #searching for packet in messages from switch to controller
    conn.write_channel("echo mininet | sudo -S ovs-ofctl dump-ports s1 1 -O OpenFlow13\n")
    time.sleep(1)
    output1 = conn.read_channel()
    #print(output1)
    if "word" in output1:
        conn.write_channel("mininet\n")
        time.sleep(1)    

    #searching for n_packets in the dump-flows output    
    reg1 = r'(?m)(?<=\brx pkts=)\d+'
    match1 = re.findall(reg1,output1)
    print('Number of Rx packets of port1 of switch1 in this iteration is: {}'.format(match1[0]))
    if len(y1)>0:
        temp1 = int(match1[0])
        x1.append(y1_length*5)
    else:
        temp1 = int(match1[0])
        
    y1.append(temp1)
    y1_length += 1

    y2_length = len(y2)
    
    #searching for packet in messages from switch to controller
    conn.write_channel("echo mininet | sudo -S ovs-ofctl dump-ports s1 1 -O OpenFlow13\n")
    time.sleep(1)
    output2 = conn.read_channel()
    #print(output2)
    if "word" in output2:
        conn.write_channel("mininet\n")
        time.sleep(1)    

    #searching for n_packets in the dump-flows output    
    reg2 = r'(?m)(?<=\btx pkts=)\d+'
    match2 = re.findall(reg2,output2)
    print('Number of Tx packets of port1 of switch1 in this iteration is: {}'.format(match2[0]))
    if len(y2)>0:
        temp2 = int(match2[0])
        x2.append(y2_length*5)
    else:
        temp2 = int(match2[0])
        
    y2.append(temp2)
    y2_length += 1


    y3_length = len(y3)
    
    #searching for packet in messages from switch to controller
    conn.write_channel("echo mininet | sudo -S ovs-ofctl dump-flows s1 --protocols=OpenFlow13 | grep 'dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02'\n")
    time.sleep(1)
    output3 = conn.read_channel()
    #print(output3)
    if "word" in output3:
        conn.write_channel("mininet\n")
        time.sleep(1)    

    #searching for n_packets in the dump-flows output    
    reg3 = r'(?m)(?<=\bn_packets=)\d+'
    match3 = re.findall(reg3,output3)
    print('Number of matched traffic pattern sourced from H1 and destined to H2 in this iteration is: {}'.format(match3[0]))
    if len(y3)>0:
        temp3 = int(match3[0])
        x3.append(y3_length*5)
    else:
        temp3 = int(match3[0])
        
    y3.append(temp3)
    y3_length += 1


    y4_length = len(y4)
    
    #searching for packet in messages from switch to controller
    conn.write_channel("echo mininet | sudo -S ovs-ofctl dump-flows s1 --protocols=OpenFlow13 | grep 'dl_dst=00:00:00:00:00:04 actions=drop'\n")
    time.sleep(1)
    output4 = conn.read_channel()
    #print(output4)
    if "word" in output4:
        conn.write_channel("mininet\n")
        time.sleep(1)    

    #searching for n_packets in the dump-flows output    
    reg4 = r'(?m)(?<=\bn_packets=)\d+'
    match4 = re.findall(reg4,output4)
    print('Number of violation count for the block traffic flow rule to H4 in this iteration is: {}'.format(match4[0]))
    if len(y4)>0:
        temp4 = int(match4[0])
        x4.append(y4_length*5)

    else:
        temp4 = int(match4[0])
        
    y4.append(temp4)
    y4_length += 1
    
    if int(match4[0])>200:
        fromaddr="xyz@gmail.com"
        toaddrs="abcdef@gmail.com"
        
        server=smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        username="xyz@gmail.com"
        password="abcd12345"
        server.login(username,password)
    
        msgg = """\
Subject: Hey Admin

HIGH VIOLATION COUNT!!"""
        server.sendmail(fromaddr,toaddrs,msgg)
        print("Email sent!")
        server.quit()

    y5_length = len(y5)
    
    #searching for packet in messages from switch to controller
    conn.write_channel("echo mininet | sudo -S ovs-ofctl dump-flows s1 --protocols=OpenFlow13 | grep 'tcp,tp_dst=80'\n")
    time.sleep(1)
    output5 = conn.read_channel()
    #print(output5)
    if "word" in output5:
        conn.write_channel("mininet\n")
        time.sleep(1)    

    #searching for n_packets in the dump-flows output    
    reg5 = r'(?m)(?<=\bn_packets=)\d+'
    match5 = re.findall(reg5,output5)
    print('Number of HTTP packets at switch1 in this iteration is: {}'.format(match5[0]))
    if len(y5)>0:
        temp5 = int(match5[0])
        x5.append(y5_length*5)
    else:
        temp5 = int(match5[0])
        
    y5.append(temp5)
    y5_length += 1


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

    #plot graph1
    p1.plot(x1,y1)
    p1.title("OpenFlow Switch1 Port1 Rx Montitor")
    p1.xlabel("Time(s)")
    p1.ylabel("Rx Packets Count")

    #parse graph1 to flask
    bitholder1 = []
    img_src1 = io.BytesIO()
    p1.savefig(img_src1,format='png')
    img_src1.seek(0)
    base_url1 = base64.b64encode(img_src1.getvalue()).decode()
    p1.close()
    bitholder1.append('data:image/png;base64,{}'.format(base_url1))
    
    #plot graph2
    p2.plot(x2,y2)
    p2.title("OpenFlow Switch1 Port1 Tx Montitor")
    p2.xlabel("Time(s)")
    p2.ylabel("Tx Packets Count")

    #parse graph2 to flask
    bitholder2 = []
    img_src2 = io.BytesIO()
    p2.savefig(img_src2,format='png')
    img_src2.seek(0)
    base_url2 = base64.b64encode(img_src2.getvalue()).decode()
    p2.close()
    bitholder2.append('data:image/png;base64,{}'.format(base_url2))
    
    #plot graph3
    p3.plot(x3,y3)
    p3.title("Match-Action Traffic Pattern Between H1 and H2")
    p3.xlabel("Time(s)")
    p3.ylabel("Matched Traffic Count")

    #parse graph3 to flask
    bitholder3 = []
    img_src3 = io.BytesIO()
    p3.savefig(img_src3,format='png')
    img_src3.seek(0)
    base_url3 = base64.b64encode(img_src3.getvalue()).decode()
    p3.close()
    bitholder3.append('data:image/png;base64,{}'.format(base_url3))
    
    #plot graph4
    p4.plot(x4,y4)
    p4.title("Firewall Traffic Montitor - Block traffic to H4")
    p4.xlabel("Time(s)")
    p4.ylabel("Violation Count")

    #parse graph4 to flask
    bitholder4 = []
    img_src4 = io.BytesIO()
    p4.savefig(img_src4,format='png')
    img_src4.seek(0)
    base_url4 = base64.b64encode(img_src4.getvalue()).decode()
    p4.close()
    bitholder4.append('data:image/png;base64,{}'.format(base_url4))
    
    #plot graph5
    p5.plot(x5,y5)
    p5.title("Web Traffic Montitor")
    p5.xlabel("Time(s)")
    p5.ylabel("HTTP Packet Count")

    #parse graph5 to flask
    bitholder5 = []
    img_src5 = io.BytesIO()
    p5.savefig(img_src5,format='png')
    img_src5.seek(0)
    base_url5 = base64.b64encode(img_src5.getvalue()).decode()
    p5.close()
    bitholder5.append('data:image/png;base64,{}'.format(base_url5))
    
    
    return render_template('pkt_in_gui.html',my_image = bitholder[0],my_image1 = bitholder1[0],my_image2 = bitholder2[0],my_image3 = bitholder3[0],my_image4 = bitholder4[0],my_image5 = bitholder5[0])

if __name__=="__main__":
    print("******** SDN GUI running")
    app.run(debug=True)

