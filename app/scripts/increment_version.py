# -*- coding: utf-8 -*-

# take in an argument from the command line
import sys
from dotenv import load_dotenv
import os

load_dotenv()

# input can be PATCH, MINOR, or MAJOR
# PATCH will increment the last number in the version
# MINOR will increment the middle number in the version
# MAJOR will increment the first number in the version

input = sys.argv[1]

# validate the input
if input not in ['PATCH', 'MINOR', 'MAJOR']:
    print("Invalid input. Please enter PATCH, MINOR, or MAJOR")
    sys.exit(1)

# take the env var VERSION and split it by the period
# this will give us an array of the version numbers
version = os.environ['VERSION'].split('.')

# convert the version numbers to integers
version = [int(i) for i in version]

# increment the version number based on the input
if input == 'PATCH':
    version[2] += 1
elif input == 'MINOR':
    version[1] += 1
    version[2] = 0
else:
    version[0] += 1
    version[1] = 0
    version[2] = 0

# convert the version numbers back to strings
version = [str(i) for i in version]

# join the version numbers with periods
version = '.'.join(version)

# print the new version
print(version)

# write the new version to the .env file
with open('.env', 'r') as f:
    lines = f.readlines()

with open('.env', 'w') as f:
    for line in lines:
        if 'VERSION' in line:
            f.write(f"VERSION={version}\n")
        else:
            f.write(line)

# export the new version as an environment variable
os.environ['VERSION'] = version