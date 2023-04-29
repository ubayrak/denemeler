#!/usr/bin/env python3

import telnetlib
import time
import datetime

now = datetime.datetime.now()
log_file = f"log_file_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"


komut = "wb_cli -s info"

# Open a file for writing the Telnet output
with open(log_file, 'w') as f:
    with telnetlib.Telnet('192.168.1.200', 23) as tn:
        time.sleep(2)
        tn.write('oem'.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write('BytelOem'.encode('ascii') + b"\n")
        time.sleep(2)
        tn.read_until(b"/ $").decode('ascii')

        tn.write(komut.encode('ascii') + b"\n")
        time.sleep(1)
        tn.read_until(b"\n").decode('ascii')
        time.sleep(2)
        # print(tn.read_until(b"/ $").decode('ascii'))
        while True:
            line = tn.read_until(b"\n").decode('ascii')
            # Write each line of Telnet output to the log file
            f.write(line)
