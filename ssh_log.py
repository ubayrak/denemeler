import paramiko

HOST = "192.168.50.254"
USERNAME = "oem"
PASSWORD = "BytelOem"  # Or use key authentication

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USERNAME, password=PASSWORD)
    transport = client.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    channel.exec_command("logread -f")

    try:
        while True:
            if channel.recv_ready():
                output = channel.recv(4096).decode("utf-8", errors="ignore")
                print(output, end="")
    except KeyboardInterrupt:
        print("\nSession closed.")
    finally:
        channel.close()
        client.close()

if __name__ == "__main__":
    main()