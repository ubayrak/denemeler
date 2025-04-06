from time import sleep
import os

filecount = int(os.popen(f'find . -maxdepth 1 -type f | wc -l').read().strip())

print(filecount)
