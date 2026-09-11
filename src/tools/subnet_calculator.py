import subprocess
import ipaddress
import requests
import re


address = input(
        "\nSubnet Calculator\n"
        "----------------------------------------\n"
        "Enter the IP address\n"
        "  e.g. 192.168.1.0/24\n"
        "\n"
        "> "
    )
subnets = int(input(
        "\nEnter the number of subnets\n"
        "  e.g. 4\n"
        "\n"
        "> "
    ))

prefix = int(address.split("/", 1)[1])
print(prefix)

count = 1
complete = False

while not complete:

    if 2**count >= subnets:
        complete = True
    else:
        count += 1

new_prefix = prefix + count
print(new_prefix)

subnet_mask = ""
bit_count = 0

for i in range(new_prefix):
    if(i % 8 == 0 and i != 1 and i != 0):
        subnet_mask += "."

    bit_count += 1
    subnet_mask += '1'

for i in range(32-bit_count):
    subnet_mask += '0'

print(subnet_mask)

print("New subnet mask:")
decimal_mask = ".".join(str(int(octet, 2)) for octet in subnet_mask.split("."))
print(decimal_mask)  
