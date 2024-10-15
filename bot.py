import asyncio
import requests
import random
import urllib.parse
import json
import os
import time
import signal
from colorama import Fore, Style, init
from datetime import datetime
import aiohttp
import re
from fake_useragent import UserAgent

# Initialize colorama for color output
init(autoreset=True)

# Global variable to control the main loop
running = True

red = Fore.LIGHTRED_EX
wht = Fore.LIGHTWHITE_EX
grn = Fore.LIGHTGREEN_EX
yel = Fore.LIGHTYELLOW_EX
blu = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
blc = Fore.LIGHTBLACK_EX
last_log_message = None


def log(message):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"{blc}[{now}]{wht} {message}{reset}")

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{wht}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{wht}please wait until {h}:{m}:{s} ", flush=True, end="\r")

def signal_handler(signum, frame):
    global running
    running = False
    log("Received interrupt signal. Preparing to exit...")

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    log("File 'config.json' not found.")

min_click = int(config.get("min_click", 50))
max_click = int(config.get("max_click", 70))
min_delay_click = int(config.get("min_delay_click", 1))
max_delay_click = int(config.get("max_delay_click", 3))
use_proxy = config.get("use_proxy", False)
workers = int(config.get("workers", 5))
countdown_loop = int(config.get("countdown_loop", 10))

sema = asyncio.Semaphore(workers)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


def get_headers(cookie=None):
    headers = {
        'User-Agent': UserAgent(os='android').random,
        'Accept': 'application/json'
    }
    if cookie:
        headers["cookie"] = cookie
    return headers

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def _banner():
    banner = r"""
  _____   _    _    _____   _    _   __  __   ____    ______   _____  
 / ____| | |  | |  / ____| | |  | | |  \/  | |  _ \  |  ____| |  __ \ 
| |      | |  | | | |      | |  | | | \  / | | |_) | | |__    | |__) |
| |      | |  | | | |      | |  | | | |\/| | |  _ <  |  __|   |  _  / 
| |____  | |__| | | |____  | |__| | | |  | | | |_) | | |____  | | \ \ 
 \_____|  \____/   \_____|  \____/  |_|  |_| |____/  |______| |_|  \_\ """
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(grn + f" xKuCoin Telegram Bot")
    print(red + f" FREE TO USE = Join us on {wht}t.me/cucumber_scripts")
    print(red + f" before start please '{grn}git pull{red}' to update bot")
    log_line()

def log_line():
    print(wht + "~" * 60)


def read_data_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            encoded_data = line.strip()
            if encoded_data:
                accounts.append(encoded_data)
    return accounts

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

async def get_public_ip():
    url = "https://httpbin.org/ip"  # You can also use "https://ipinfo.io/ip"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            ip_info = await response.json()
            return ip_info['origin']  # This returns the public IP address

def decode_data(encoded_data):
    params = dict(item.split('=') for item in encoded_data.split('&'))
    decoded_user = urllib.parse.unquote(params['user'])
    decoded_start_param = urllib.parse.unquote(params['start_param'])
    return {
        "decoded_user": decoded_user,
        "decoded_start_param": decoded_start_param,
        "hash": params['hash'],
        "auth_date": params['auth_date'],
        "chat_type": params['chat_type'],
        "chat_instance": params['chat_instance']
    }


async def login(decoded_data, proxy=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/login?lang=en_US"
    headers = get_headers()
    body = {
        "inviterUserId": "5496274031",
        "extInfo": {
            "hash": decoded_data['hash'],
            "auth_date": decoded_data['auth_date'],
            "via": "miniApp",
            "user": decoded_data['decoded_user'],
            "chat_type": decoded_data['chat_type'],
            "chat_instance": decoded_data['chat_instance'],
            "start_param": decoded_data['decoded_start_param']
        }
    }

    session = requests.Session()
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}

    try:
        response = session.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an error for bad responses
        cookie = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
        return cookie

    except requests.exceptions.RequestException as e:
        print(Fore.LIGHTBLACK_EX + f" Proxy failed: {proxy}. Error: {str(e)}. Trying random proxy...")
        return None

    except aiohttp.ClientError as e:  # Catching aiohttp specific exceptions
        log(f'Proxy failed: {proxy}. Error: {str(e)}. Trying random proxy...')
        return None



async def fetch_data(cookie, account_index, username, proxy=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"
    headers = get_headers(cookie=cookie)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            data = await response.json()
            if data.get("success"):
                balance = data.get("data", {}).get("availableAmount")
                molecule = data.get("data", {}).get("feedPreview", {}).get("molecule")
                log(grn + f"Account {wht}{account_index}  | {grn}User - {wht}{username} | {yel}Balance: {wht}{balance}")
                return molecule, balance
            else:
                return None, None


async def tap(cookie, molecule, account_index, proxy=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/gold/increase?lang=en_US"
    headers = get_headers(cookie=cookie)

    total_increment = 0

    while total_increment < 3000 and running:
        increment = random.randint(min_click, max_click)
        form_data = {
            'increment': str(increment),
            'molecule': str(molecule)
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=form_data, proxy=proxy) as response:



                    total_increment += increment

                    log(yel + f"Account {wht}{account_index} | {blu}Tapped: {wht}{increment} | {blu}Total Tap: {wht}{total_increment}/3000")
                    sleep = random.randint(min_delay_click, max_delay_click)
                    await asyncio.sleep(sleep)

        except requests.exceptions.RequestException:
            print(
                Fore.LIGHTBLACK_EX + f"Network error occurred. Retrying...")
            await asyncio.sleep(5)



async def process_account(encoded_data, account_index, total_balance, broken_accounts, proxies):
    async with sema:  # Limit concurrency using semaphore

        try:
            try:
                decoded_data = decode_data(encoded_data)
                decoded_user_json = json.loads(decoded_data['decoded_user'])
                username = decoded_user_json.get('username')
            except:
                log(red + f'Bad query. Account {wht}{account_index} ')
                broken_accounts.append(account_index)
                username = None

            if use_proxy and len(proxies) > 0:
                proxy_index = account_index % len(proxies)
                proxy = proxies[proxy_index]
                pattern = r'(\d+\.\d+\.\d+\.\d+:\d+)'
                show_proxy = re.search(pattern, proxy).group(1)
            else:
                show_proxy = False
                proxy=None

            if username:
                log(grn + f"Try auth Account {wht}{account_index}  | {grn}User - {wht}{username} | {grn} Proxy: {wht}{show_proxy}")

                cookie = await login(decoded_data, proxy)

                if not cookie and use_proxy:
                    proxy = random.choice(proxies)
                    cookie = await login(decoded_data, proxy)

                if cookie:  # Proceed only if login was successful.
                    molecule, balance = await fetch_data(cookie, account_index, username, proxy)
                    if balance:
                        total_balance.append(balance)
                        await tap(cookie, molecule, account_index, proxy)
                    else:
                        log(red + f'Need update query! Account {wht}{account_index}')
                        broken_accounts.append(account_index)


        except Exception as e:
            log(red + f" An unexpected error occurred while processing Account {wht}{account_index}  "
                      f"/ {grn}User - {wht}{username}: {str(e)}")


async def main():
    global running
    file_path_accounts = "data.txt"
    file_path_proxies = "proxies.txt"

    encoded_data_list = read_data_file(file_path_accounts)
    proxies = read_proxies(file_path_proxies)

    _clear()
    _banner()
    log(blu + f'Total accounts: {wht}{len(encoded_data_list)} | {blu} Workers {wht}{workers} ')
    log(blu + f'Total proxies: {wht}{len(proxies)} | {blu}Use proxy: {wht}{use_proxy}')
    if len(proxies) == 0:
        log(red + f'No proxy found! Proxy = False')
    log_line()
    broken_accounts = []

    try:
        while running:

            total_balance = []

            tasks = [
                asyncio.create_task(process_account(encoded_data, index, total_balance, broken_accounts, proxies))
                for index, encoded_data in enumerate(encoded_data_list, start=1) if not index in broken_accounts]

            await asyncio.gather(*tasks)

            if running:
                log_line()
                log(red + f'Total Balance: {wht}{sum(total_balance)}')
                log(red + f'total_broken: {wht}{len(broken_accounts)} / {len(encoded_data_list)}{red} broken_accounts:{wht}{broken_accounts}')
                log_line()
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                open("error.txt", "a", encoding="utf-8").write(
                    f"{now} / total_broken: {len(broken_accounts)} / {len(encoded_data_list)} broken_accounts:{broken_accounts} \n"
                )
                log(yel + f"Waiting for {wht}{countdown_loop} sec before next cycle...")
                countdown_timer(countdown_loop)
                await asyncio.sleep(0)

    except Exception as e:
        log(
            Fore.LIGHTBLACK_EX + f"An unexpected error occurred: {str(e)}")

    finally:
        log(
            Fore.LIGHTBLACK_EX + f"Successfully logged out from bot. Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())