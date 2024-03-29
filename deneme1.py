import telnetlib
import time


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
        self.connection.write('sh'.encode('ascii') + b"\n")
        time.sleep(2)
        self.connection.write(b"\n")
        time.sleep(1)
        self.connection.read_very_eager().decode('ascii') # clears read buffer so far


    def command(self, comm : str):
        self.comm = comm
        self.connection.write(comm.encode('ascii') + b"\n")
        time.sleep(2)
        return self.connection.read_until(b"#").decode('ascii')


    def close(self):
        self.connection.close()

host = '192.168.1.5'
port = 23
username = 'admin'
password = 'Admin123'
conn = TelnetConnection(host, port, username, password)
conn.connect()
print(conn.command("wb_cli -s info"))