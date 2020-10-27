#!/bin/bash

runtime="5 minute"
endtime=$(date -ud "$runtime" +%s)
while [[ $(date -u +%s) -le $endtime ]]
do
        echo "`tshark -i enp0s9 -d tcp.port==6633,openflow -O openflow_v4 -Y 'openflow_v4.type==10'  -T fields -e ip.src -e tcp.srcport >> logging_ip.txt`"
done
