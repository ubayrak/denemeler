import telnetlib
import time

komut=''


with telnetlib.Telnet('192.168.1.200', 23) as tn:
    time.sleep(2)
    tn.write('oem'.encode('ascii') + b"\n")
    time.sleep(1)
    tn.write('BytelOem'.encode('ascii') + b"\n")
    time.sleep(3)
    tn.write(komut.encode('ascii') + b"\n")
    time.sleep(2)
    output=tn.read_very_eager().decode('ascii')
    time.sleep(1)

