import requests
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

def type_effect(text, delay=0.002):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

# ========= CONFIG =========
API_KEY = "1DFD854EB3DA45C7A46DB9CFA2DB12C8"

# ========= FUNCTIONS =========
def slow_print(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.01)
    print()
    
def show_osint_links(number):
    print("\n🔍 ===== OSINT SEARCH LINKS =====\n")
    
    print(f"🌐 Google       : https://www.google.com/search?q={number}")
    print(f"📞 Truecaller   : https://www.truecaller.com/search/in/{number}")
    print(f"💬 WhatsApp     : https://wa.me/{number}")
    print(f"📢 Telegram     : https://t.me/{number}")
    
    print("\n===============================\n")

def show_banner():
    os.system("clear")
    ascii_banner = f"""{Fore.GREEN}


 _  __   _    __  __    _    _    _    ____     __        __   ___   ____   _      ____  
| |/ /  / \  |  \/  |  / \  | |  | | / ___|     \ \      / /  / _ \ |  _ \ | |    |  _ \ 
| ' /  / _ \ | |\/| | / _ \ | |   _  \___ \      \ \ /\ / /  | | | || |_) || |    | | | |
| . \ / ___ \| |  | |/ ___ \| |___    ___) |      \ V  V /   | |_| ||  _ < | |___ | |_| |
|_|\_/_/   \_\_|  |_/_/   \_\_____|  |____/        \_/\_/     \___/ |_| \_\|_____||____/ 

"""
    type_effect(ascii_banner, delay=0.01)

    credit = f"{Fore.RED}{Style.BRIGHT}➤ Credit by KAMAL SINGH MAURYA\n"
    print(credit)
    type_effect("🔍 Initializing system...\n", 0.01)
    time.sleep(0.5)
    type_effect("⚡ Loading modules...\n", 0.01)
    
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

def get_number_info(number):
    url = f"https://api.veriphone.io/v2/verify?phone={number}&key={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        print("\n📊 ===== RESULT =====\n")
        print(f"📞 Number      : {number}")
        print(f"🌍 Country     : {data.get('country')}")
        print(f"📡 Carrier     : {data.get('carrier')}")
        print(f"📱 Phone Type  : {data.get('phone_type')}")
        print(f"✅ Valid       : {data.get('phone_valid')}")
        print("\n====================\n")
        
        show_osint_links(number)

    except Exception as e:
        print("❌ Error:", e)
        
    
      
# ========= MAIN =========
show_banner()

number = input("👉 Enter Mobile Number (with country code): ")
get_number_info(number)
