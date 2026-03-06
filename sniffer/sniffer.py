import serial
import time
import subprocess
import logging
from datetime import datetime
from collections import deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# In-memory log storage for GUI display
log_messages = deque(maxlen=100)

def add_log(message, level="INFO"):
    """Add message to both logger and GUI log buffer"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {level}: {message}"
    log_messages.append(formatted_msg)
    
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
    else:
        logging.debug(message)

def get_logs():
    """Return all current logs as a list"""
    return list(log_messages)

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
    "6GHz": "160",
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
    return f"tcpdump -i {radiotaps[band]} -n -w - | nc 192.168.2.228 {ports[band]} &\n"
def set_channel_cmd(band, channel):
    return f" wl -i {interfaces[band]} chanspec {channel}/{bandwidths[band]}\n"



class SnifferController:

    def __init__(self):
        try:
            self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
            self.running_processes = []
            self.capture_files = {}  # Track capture files for each band
            add_log("Serial connection established at /dev/ttyUSB0")
            time.sleep(2)  # Wait for serial connection to establish
            add_log("Ready to control sniffing machine")
        except Exception as e:
            add_log(f"Failed to establish serial connection: {str(e)}", "ERROR")
            raise
    
    def start_sniff_machine(self):
        add_log("Starting sniff machine...")
        self.ser.write(sniff_start.encode())
        add_log("Sniff machine startup command sent, waiting 12 seconds for boot...")
        time.sleep(12)
        add_log("Sniff machine started successfully")
        
    def start_band(self, band, channel):
        try:
            add_log(f"Starting band: {band} on channel {channel}")
            
            # 1️⃣ Start PC listener
            pc_cmd = f"nc -l -p {ports[band]} > Capture_{band}.pcap &"
            add_log(f"Starting PC listener for {band} on port {ports[band]}")
            p = subprocess.Popen(pc_cmd, shell=True)
            self.running_processes.append(p)
            add_log(f"PC listener process started (PID: {p.pid})")

            time.sleep(2)

            # 2️⃣ Set channel
            channel_cmd = f"wl -i {interfaces[band]} chanspec {channel}/{bandwidths[band]}\n"
            add_log(f"Setting channel: {channel}/{bandwidths[band]} MHz on interface {interfaces[band]}")
            self.ser.write(channel_cmd.encode())

            time.sleep(3)
            add_log(f"Channel set successfully for {band}")

            # 3️⃣ Start tcpdump on device
            tcpdump_cmd = f"tcpdump -i {radiotaps[band]} -n -w - | nc 192.168.2.228 {ports[band]} &\n"
            add_log(f"Starting tcpdump capture on interface {radiotaps[band]}")
            self.ser.write(tcpdump_cmd.encode())
            add_log(f"tcpdump started, streaming to 192.168.2.228:{ports[band]}")
            
            # Track the capture file
            self.capture_files[band] = f"Capture_{band}.pcap"
            
        except Exception as e:
            add_log(f"Error starting band {band}: {str(e)}", "ERROR")

    def stop_sniff_machine(self):
        add_log("Stopping sniff machine...")
        self.ser.write(sniff_stop.encode())
        add_log("Sniff machine stop command sent, waiting 3 seconds...")
        time.sleep(3)
        add_log("Sniff machine stopped")
        add_log("Capture files saved in the directory: /home/test/Sniffer/")


    def stop_all(self):
        add_log("Stopping all capture processes...")
        add_log("Sending killall tcpdump command")
        self.ser.write(b"killall tcpdump\n")
        time.sleep(1)
        
        add_log("Sending killall nc command")
        self.ser.write(b"killall nc\n")
        time.sleep(1)

        add_log(f"Terminating {len(self.running_processes)} local processes")
        for p in self.running_processes:
            p.terminate()
            add_log(f"Terminated process PID: {p.pid}")

        self.running_processes.clear()
        add_log("All capture processes stopped successfully")

    def get_capture_files(self):
        """Return dictionary of capture files by band"""
        return self.capture_files.copy()

    def clear_capture_files(self):
        """Clear the capture files tracking"""
        self.capture_files.clear()
        add_log("Capture file tracking cleared")



"""
subprocess.Popen(pc_cmd, shell=True)
time.sleep(3)

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
ser.write(cmd.encode())
time.sleep(10)
"""
