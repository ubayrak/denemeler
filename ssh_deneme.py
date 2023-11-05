import paramiko
import sys
import time

# Define your SSH connection details
hostname = "192.168.1.254"
port = 22
username = "oem"
password = "BytelOem"
i=1
# Create an SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the SSH server
    client.connect(hostname, port, username, password)

    # Start an interactive session
    ssh_session = client.invoke_shell()

    print("SSH session established. Type 'exit' to exit the session.")

    while True:
        # Read user input from the keyboard
        # user_input = input("Enter a command: ")
        time.sleep(2)
        user_input = "airdata-cli -e 'GetParameterValues Device.X_AIRTIES_Obj.MultiAPController.SSIDProfile.3.KeyPassphrase'"

        if i == 2:
            break  # Exit the session

        # Send the user's input as a command
        ssh_session.send(user_input + "\n")
        time.sleep(3)
        # Read and print the output
        output = ssh_session.recv(65535).decode()
        print("Command Output:")
        print(output)
        i+=1

    # Close the SSH session
    ssh_session.close()

except paramiko.AuthenticationException:
    print("Authentication failed.")
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
except KeyboardInterrupt:
    print("Session terminated by user.")
finally:
    # Close the SSH connection
    client.close()
