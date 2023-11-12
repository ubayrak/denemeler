import paramiko
import time
import re


class SSHConnection:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
            print(f"Connected to {self.hostname}")
        except paramiko.AuthenticationException:
            print(f"Failed to connect to {self.hostname}. Authentication failed.")
        except paramiko.SSHException as e:
            print(f"Error connecting to {self.hostname}: {str(e)}")

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def close(self):
        self.client.close()

# Example usage
if __name__ == "__main__":
    ssh = SSHConnection("192.168.1.254", 22, "oem", "BytelOem")
    ssh.connect()

    result = ssh.execute_command("wb_cli -s info")
    print(result)

    ssh.close()
