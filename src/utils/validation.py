import time
from tools.scanner import scan

def get_int_input(lower_bound, upper_bound):
    try:
        response = int(input())
    except ValueError:
        print("\n[!] Please enter a number")
        time.sleep(1)
        return

    if not lower_bound <= response <= upper_bound:
        print(f"\n[!] Enter a number between {lower_bound} and {upper_bound}")
        time.sleep(1)
        return

    return response

def check_ip():
    response = input()
    
    if not response.count(".") == 3:
        print("[!] Please enter a valid IP address.")
        return None
    if scan(response) == None:
        print("[!] IP not found on your network. Check you have entered it correctly.")
        return None
    
    return response

def get_yes_no(prompt="Continue? [Y/n]: "):
    while True:
        response = input(prompt).strip().lower()

        if response in ("y", "yes", ""):
            return True
        if response in ("n", "no"):
            return False
        
        print("[!] Please enter y/n.")