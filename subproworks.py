import subprocess


command = 'telnet 10.30.37.120 11 &'
result = subprocess.run(command, shell=True)

#result = subprocess.run(['telnet 10.30.37.120 11'], capture_output=True, text=True, shell=True)
print(result.stdout)


