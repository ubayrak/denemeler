import serial
import time
import subprocess

pc_cmd= "nc -l -p 9999 > Capture5G.pcap &"

sniff_start="sniff.sh start\n"
sniff_stop="sniff.sh stop\n"
cmd="tcpdump -i radiotap1 -n -w - | nc 192.168.2.22 9999 &\n"

subprocess.Popen(pc_cmd, shell=True)
time.sleep(3)

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
# ser.write(b"fwversion\n")
ser.write(cmd.encode())
time.sleep(10)


# print(ser.read_all().decode())
