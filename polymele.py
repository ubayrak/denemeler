import telnetlib
import time

komut='wb_cli -s info'


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
    print(tn.read_until(b"/ $").decode('ascii'))

