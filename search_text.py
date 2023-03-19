#!/usr/bin/env python3

import glob

directory_path = '/home/ubayrak/Desktop/Commands'
keyword = 'bs_data'

files = glob.glob(directory_path + '**/*', recursive=True)



for file_path in files:
    with open(file_path, 'r') as file:
        contents = file.read()
        if keyword in contents:
            print(f'Found keyword "{keyword}" in file: {file_path}')