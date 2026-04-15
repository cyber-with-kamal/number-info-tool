import requests
import json
import os
import time
import random
from colorama import init, Fore, Style

init(autoreset=True)

# === CONFIGURATION ===
API_BASE = "http://apilayer.net/api/validate?access_key=YOUR_API_KEY&number="


## Target
192.168.64.2

## Command Used
nmap -sS -sV -O 192.168.64.2

## Results
- All ports are closed
- No open services found

## Screenshot
![Output](nmap_output.png)

## Note
Scanning performed in a controlled environment

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://anish-axploits.vercel.app/",
    "Connection": "keep-alive"
}

# === Typing Animation ===
def type_effect(text, delay=0.002):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# === Swipe-style Text Animation ===
def swipe_effect(text, delay=0.01):
    for line in text.splitlines():
        for char in line:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

# === Banner ===
def show_banner():
    os.system("clear")
    ascii_banner = f"""{Fore.GREEN}


 _  __   _    __  __    _    _    _    ____     __        __   ___   ____   _      ____  
| |/ /  / \  |  \/  |  / \  | |  | | / ___|     \ \      / /  / _ \ |  _ \ | |    |  _ \ 
| ' /  / _ \ | |\/| | / _ \ | |   _  \___ \      \ \ /\ / /  | | | || |_) || |    | | | |
| . \ / ___ \| |  | |/ ___ \| |___    ___) |      \ V  V /   | |_| ||  _ < | |___ | |_| |
|_|\_/_/   \_\_|  |_/_/   \_\_____|  |____/        \_/\_/     \___/ |_| \_\|_____||____/ 

"""
    credit = f"{Fore.RED}{Style.BRIGHT}➤ Credit by KAMAL SINGH MAURYA\n"
    type_effect(ascii_banner, delay=0.0005)
    print(credit)

# === JavaScript-style Formatter ===
def format_as_js(data):
    js_lines = []
    # preserve order if it's an OrderedDict otherwise just iterate
    for key, value in data.items():
        key_str = key
        # pretty JSON-style for values
        value_str = json.dumps(value, ensure_ascii=False)
        js_lines.append(f"  {key_str}: {value_str}")
    return "{\n" + ",\n".join(js_lines) + "\n}"

# === Random Color Swipe Printer ===
def print_colored(text, delay=0.005):
    colors = [Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX]
    for line in text.splitlines():
        color = random.choice(colors)
        for char in line:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print()

# === Normalize API response into list of dicts ===
def normalize_response(data):
    """
    Accepts the parsed JSON `data` and returns a list of record-dicts to display.
    Tries several common shapes so it is robust to small API changes.
    """
    # If the API already returns {'data': [...]}
    if isinstance(data, dict) and "data" in data and data["data"]:
        if isinstance(data["data"], list):
            return data["data"]
        # sometimes data can be a single dict
        if isinstance(data["data"], dict):
            return [data["data"]]

    # If API returns a list at top level
    if isinstance(data, list):
        return data

    # If API returns a single dict with useful fields, wrap it
    if isinstance(data, dict):
        # If dict contains keys that look like user info, return as single record
        likely_keys = {"name", "title", "mobile", "number", "operator", "circle", "state", "sim"}
        if likely_keys.intersection(set(data.keys())):
            return [data]

        # If nested under other keys, try to find the first list/dict child
        for k, v in data.items():
            if isinstance(v, list) and v:
                return v
            if isinstance(v, dict) and v:
                return [v]

    # Fallback: return empty list
    return []

# === Search Function (API) ===
def search_number(number):
    url = f"{API_BASE}{number}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        raw_text = response.text.strip()

        # Try direct JSON parse first
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            # If the API returns stray characters around JSON, try to extract the first {...} block
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    data = json.loads(raw_text[start:end+1])
                except Exception:
                    print(Fore.RED + "⚠️ Unable to parse JSON response from server.")
                    return
            else:
                print(Fore.RED + "⚠️ Invalid response format from server.")
                return

        records = normalize_response(data)

        if not records:
            print(Fore.YELLOW + "⚠️ No results found.")
            return

        swipe_effect(Fore.CYAN + f"\n📊 Search Results for {number}\n")

        for idx, user in enumerate(records, 1):
            title = f"=== [ RESULT {idx} ] ==="
            type_effect(Fore.LIGHTRED_EX + title)

            # Ensure `user` is a dict before formatting
            if isinstance(user, dict):
                formatted = format_as_js(user)
                print_colored(formatted)
            else:
                # if user is a primitive or unexpected type, just print it
                type_effect(Fore.YELLOW + str(user))

        print(Fore.RED + "\n⚡ Made by KAMAL SINGH MAURYA")

    except requests.exceptions.ReadTimeout:
        print(Fore.RED + "⚠️ Server Timeout. Try again later.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"⚠️ Network error: {e}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Error: {e}")

# === Main CLI ===
def main():
    os.system("clear")
    show_banner()
    while True:
        try:
            type_effect(Fore.BLUE + "\n📞 Enter Your 10 Digit Number (or 'exit' to quit):")
            number = input(Fore.LIGHTGREEN_EX + "Target ➤ ")
            if number.lower() == "exit":
                break
            if number.isdigit() and len(number) == 10:
                search_number(number)
            else:
                print(Fore.RED + "❌ Invalid number. Please enter exactly 10 digits.")
        except KeyboardInterrupt:
            print(Fore.RED + "\n⛔ Exiting...")
            break

# === Entry Point ===
if __name__ == "__main__":
    main()
