from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
import sys
import configparser
import csv
import time

# Define color codes (these might not work properly on Windows CMD)
re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

              Version : 1.01
 {re}Subscribe Termux Professor on Youtube.
   {cy}www.youtube.com/c/TermuxProfessorYT
        """)

# Detect OS and clear screen accordingly
def clear_screen():
    if os.name == 'nt':  # If on Windows
        os.system('cls')
    else:  # If on Linux/Unix/MacOS
        os.system('clear')

# Read credentials from config file
cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    clear_screen()
    banner()
    print(re + "[!] Run python3 setup.py first !!\n")
    sys.exit(1)

# Connect to the Telegram client
client.connect()
if not client.is_user_authorized():
    try:
        client.send_code_request(phone)
        clear_screen()
        banner()
        client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))
    except Exception as e:
        print(re + f"[!] Error: {str(e)}")
        sys.exit(1)

# Fetching group data
clear_screen()
banner()

chats = []
last_date = None
chunk_size = 200
groups = []

try:
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
except Exception as e:
    print(re + f"[!] Error fetching dialogs: {str(e)}")
    sys.exit(1)

# Filter for mega groups
for chat in chats:
    try:
        if chat.megagroup:  # Check if it's a megagroup
            groups.append(chat)
    except:
        continue

# Display groups and select one
print(gr + '[+] Choose a group to scrape members:' + re)
for i, g in enumerate(groups):
    print(gr + f'[{cy}{i}{gr}] - {g.title}')

try:
    g_index = int(input(gr + "[+] Enter a number: " + re))
    target_group = groups[g_index]
except (IndexError, ValueError):
    print(re + "[!] Invalid input, please enter a valid number.")
    sys.exit(1)

# Fetch members from the selected group
print(gr + '[+] Fetching members...')
time.sleep(1)
try:
    all_participants = client.get_participants(target_group, aggressive=True)
except Exception as e:
    print(re + f"[!] Error fetching members: {str(e)}")
    sys.exit(1)

# Save members to a CSV file
print(gr + '[+] Saving to file...')
time.sleep(1)
csv_filename = "members.csv"
try:
    with open(csv_filename, "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            username = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
    print(gr + f'[+] Members scraped successfully. Saved to {csv_filename}')
except Exception as e:
    print(re + f"[!] Error saving file: {str(e)}")

print(gr + '[+] Subscribe to Termux Professor Youtube Channel for Add Members')
