import paramiko

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
            self.client.connect(self.hostname, self.port, self.username, self.password)
            print("SSH session established.")
        except paramiko.AuthenticationException:
            print("Authentication failed.")
        except paramiko.SSHException as e:
            print("SSH connection failed:", str(e))

    def airdata_command(self, command):
        ssh_session = self.client.invoke_shell()

        try:
            # Send the user's input as a command
            ssh_session.send(command + "\n")
            
            # Read and return the output
            output = ssh_session.recv(65535).decode()
            return output
        finally:
            # Close the SSH session
            ssh_session.close()

    def close(self):
        # Close the SSH connection
        self.client.close()

if __name__ == "__main__":
    # Define your SSH connection details
    hostname = "192.168.1.254"
    port = 22
    username = "oem"
    password = "BytelOem"

    # Create an instance of SSHConnection
    ssh_connection = SSHConnection(hostname, port, username, password)

    try:
        # Connect to the SSH server
        ssh_connection.connect()

        # Define the command to execute
        command = "airdata-cli -e 'GetParameterValues Device.X_AIRTIES_Obj.MultiAPController.SSIDProfile.3.KeyPassphrase'"

        # Execute the command and print the output
        result = ssh_connection.execute_command(command)
        print("Command Output:")
        print(result)

    except KeyboardInterrupt:
        print("Session terminated by user.")
    finally:
        # Close the SSH connection
        ssh_connection.close()
