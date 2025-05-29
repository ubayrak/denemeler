import os

#filecount = int(os.popen('find . -maxdepth 1 -type f | wc -l').read().strip())

location = os.popen('pwd').read().strip()

print(location)