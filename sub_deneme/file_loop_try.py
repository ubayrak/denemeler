from time import sleep
import os

# Define file name
file_name = "/home/ugur/german.txt"

# Open file in write mode to start fresh
# with open(file_name, "w") as file:
#     file.write("Start of log file\n")
#     sleep(2)

# print("Misson accomplished.")
# print(f"{os.path.abspath(file_name)}")

linecount = int(os.popen(f'wc -l < {file_name}').read().strip())

while linecount > 0:
    linecount-=1
    print(f'now it is {linecount}')


print("Program exited.")



