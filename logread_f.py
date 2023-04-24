#!/usr/bin/env python3

import telnetlib
import time
import datetime

now = datetime.datetime.now()
log_file = f"log_file_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"


komut = "logread -f"
c1='airdata-cli -e "SetParameterValues Device.X_AIRTIES_Obj.CloudComm.AuthURL https://device-auth-bytelstg.bouygues.airtiescloud.eu/oauth/token"'
c2="airdata-cli -e 'SetParameterValues Device.X_AIRTIES_Obj.CloudComm.AuthPassword f7db109d-ff8d-4f7d-aac1-e156c9523559$BtYpKWKuKRJLu6tys5ZdmD8t7PDY1Fcz'"
c3='airdata-cli -e "SetParameterValues Device.X_AIRTIES_Obj.CloudComm.ChallengeURL https://device-auth-bytelstg.bouygues.airtiescloud.eu/challenge"'



# Open a file for writing the Telnet output
with open(log_file, 'w') as f:
    with telnetlib.Telnet('192.168.1.200', 23) as tn:
        time.sleep(2)
        tn.write('oem'.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write('BytelOem'.encode('ascii') + b"\n")
        time.sleep(2)
        tn.read_until(b"/ $").decode('ascii')
        
        tn.write(c1.encode('ascii') + b"\n")
        time.sleep(2)
        tn.read_until(b"\n").decode('ascii')
        time.sleep(2)       
        tn.write(c2.encode('ascii') + b"\n")
        time.sleep(2)
        tn.read_until(b"\n").decode('ascii')
        time.sleep(2) 
        tn.write(c3.encode('ascii') + b"\n")
        time.sleep(2)
        tn.read_until(b"\n").decode('ascii')
        time.sleep(3) 

        tn.write(komut.encode('ascii') + b"\n")
        time.sleep(1)
        tn.read_until(b"\n").decode('ascii')
        time.sleep(2)
        while True:
            line = tn.read_until(b"\n").decode('ascii')
            # Write each line of Telnet output to the log file
            f.write(line)

