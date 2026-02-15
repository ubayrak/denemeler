import serial
import time
import subprocess
import logging

radiotaps = {
    "6GHz": "radiotap2",
    "2.4GHz": "radiotap1",
    "5GHz": "radiotap0"
}
interfaces = {
    "6GHz": "wl2",
    "2.4GHz": "wl1",
    "5GHz": "wl0"
}
bandwidths = {
    "6GHz": "320",
    "2.4GHz": "20",
    "5GHz": "80"
}
ports = {
    "6GHz": "9999",
    "2.4GHz": "9998",
    "5GHz": "9997"
}

# COMMANDS
sniff_start="sniff.sh start\n"
sniff_stop="sniff.sh stop\n"
def set_PC_cmd(band):
    return f"nc -l -p {ports[band]} > Capture{band}.pcap &"
def set_tcpdump_cmd(band):
    return f"tcpdump -i {radiotaps[band]} -n -w - | nc 192.168.2.22 {ports[band]} &\n"
def set_channel_cmd(band, channel):
    return f" wl -i {interfaces[band]} chanspec {channel}/{bandwidths[band]}\n"



class SnifferController:

    def __init__(self):
        self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        self.running_processes = []
        time.sleep(2)  # Wait for serial connection to establish
    
    def start_sniff_machine(self):
        self.ser.write(sniff_start.encode())
        time.sleep(12)
        
    def start_band(self, band, channel):
        # 1️⃣ Start PC listener
        pc_cmd = f"nc -l -p {ports[band]} > Capture_{band}.pcap &"
        p = subprocess.Popen(pc_cmd, shell=True)
        self.running_processes.append(p)

        time.sleep(2)

        # 2️⃣ Set channel
        channel_cmd = f"wl -i {interfaces[band]} chanspec {channel}/{bandwidths[band]}\n"
        self.ser.write(channel_cmd.encode())

        time.sleep(3)

        # 3️⃣ Start tcpdump on device
        tcpdump_cmd = f"tcpdump -i {radiotaps[band]} -n -w - | nc 192.168.2.22 {ports[band]} &\n"
        self.ser.write(tcpdump_cmd.encode())

    def stop_sniff_machine(self):
        self.ser.write(sniff_stop.encode())
        time.sleep(3)

    def stop_all(self):
        self.ser.write(b"killall tcpdump\n")
        time.sleep(1)
        self.ser.write(b"killall nc\n")
        time.sleep(1)

        for p in self.running_processes:
            p.terminate()

        self.running_processes.clear()



"""
subprocess.Popen(pc_cmd, shell=True)
time.sleep(3)

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
ser.write(cmd.encode())
time.sleep(10)
"""
