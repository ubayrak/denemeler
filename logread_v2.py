#!/usr/bin/env python3

import telnetlib
import time
import datetime


class TelnetConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.log_file = None
        
    def connect(self):
        self.connection = telnetlib.Telnet(self.host, self.port)
        time.sleep(2)
        self.connection.write(self.username.encode('ascii') + b"\n")
        time.sleep(1)
        self.connection.write(self.password.encode('ascii') + b"\n")
        time.sleep(2)
        self.connection.read_until(b"/ $").decode('ascii')

    def command(self, comm):
        self.connection.write(comm.encode('ascii') + b"\n")
        time.sleep(1)
        self.connection.read_until(b"\n").decode('ascii')
        time.sleep(2)
        return self.connection.read_until(b"/ $").decode('ascii')
        
    def read_log(self):
        self.connection.write('logread -f'.encode('ascii') + b"\n")
        time.sleep(1)
        self.connection.read_until(b"\n").decode('ascii')
        now = datetime.datetime.now()
        log_file = f"log_file_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(log_file, 'w') as f:
            while True:
                line = self.connection.read_until(b"\n").decode('ascii')
                f.write(line)

    def close(self):
        self.connection.close()


# def main():
#     host = '192.168.1.200'
#     port = 23
#     username = 'oem'
#     password = 'BytelOem'
#     c1='airdata-cli -e "SetParameterValues Device.X_AIRTIES_Obj.CloudComm.AuthURL https://device-auth-bytelstg.bouygues.airtiescloud.eu/oauth/token"'
#     c2="airdata-cli -e 'SetParameterValues Device.X_AIRTIES_Obj.CloudComm.AuthPassword f7db109d-ff8d-4f7d-aac1-e156c9523559$BtYpKWKuKRJLu6tys5ZdmD8t7PDY1Fcz'"
#     c3='airdata-cli -e "SetParameterValues Device.X_AIRTIES_Obj.CloudComm.ChallengeURL https://device-auth-bytelstg.bouygues.airtiescloud.eu/challenge"'



#     conn = TelnetConnection(host, port, username, password)
#     conn.connect()
#     # conn.command(c1)
#     # conn.command(c2)
#     # conn.command(c3)
#     conn.read_log()


# if __name__ == '__main__':
#     main()


host = '192.168.1.200'
port = 23
username = 'oem'
password = 'BytelOem'
conn = TelnetConnection(host, port, username, password)
conn.connect()
conn.read_log()

