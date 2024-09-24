#!/bin/env python3
# code by : Termux Professor

"""
You can rerun setup.py if you have added some wrong value.
"""
import os
import sys
import configparser

# Define colors (these will not work in Windows CMD, unless using color libraries like colorama)
re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

def banner():
    # Detect OS and clear screen accordingly
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Unix/Mac
        os.system('clear')

    print(f"""
    {re}╔═╗{cy}┌─┐┌┬┐┬ ┬┌─┐
    {re}╚═╗{cy}├┤  │ │ │├─┘
    {re}╚═╝{cy}└─┘ ┴ └─┘┴
    
               Version : 1.01
    {re}Subscribe Termux Professor on Youtube
    {cy}www.youtube.com/c/TermuxProfessorYT
    """)

banner()
print(gr + "[+] Installing requirements...")

# Detect OS and use appropriate pip command
if os.name == 'nt':
    os.system('python -m pip install telethon')
else:
    os.system('python3 -m pip install telethon')

banner()

# Create 'config.data' file
config_file = 'config.data'
with open(config_file, 'w') as setup:
    pass  # This will create an empty file

cpass = configparser.RawConfigParser()
cpass.add_section('cred')

# Prompt for API credentials
xid = input(gr + "[+] Enter API ID: " + re)
cpass.set('cred', 'id', xid)

xhash = input(gr + "[+] Enter Hash ID: " + re)
cpass.set('cred', 'hash', xhash)

xphone = input(gr + "[+] Enter phone number: " + re)
cpass.set('cred', 'phone', xphone)

# Save credentials to config.data
with open(config_file, 'w') as setup:
    cpass.write(setup)

print(gr + "[+] Setup complete!")
print(gr + "[+] Now you can run any tool!")
print(gr + "[+] Make sure to read docs for installation & API setup.")
print(gr + "[+] https://github.com/termuxprofessor/TeleGram-Scraper-Adder/blob/master/README.md")
