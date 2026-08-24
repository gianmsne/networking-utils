import time
from tools.scanner import scan_local, scan_for_hosts
from tools.ports import get_ports, print_ports
from tools.check_ip import lookup_ip
from utils.validation import get_int_input, check_ip, get_yes_no
import platform
from config import LOCALHOST

def print_menu():
    for _ in range(10): 
        print("\n") 
        time.sleep(0.01)
    print("----- Network Tool -----")
    print("1. Get local machine IP")
    print("2. Scan local machine for open ports")
    print("3. Scan local network for devices")
    print("4. Get IP information")
    print("0. Exit")
    print("\n>>> Enter menu item: ", end="")

def os_warning(os):
    print(f"\n\n>>> [!] Sorry, this tool does not work on {os} yet.\n")
    time.sleep(1)
    print("Returning to menu...")
    time.sleep(2)

# Bounds for state machine menu
LOWER_BOUND = 0
UPPER_BOUND = 4

def main():

    print_menu()
    response = get_int_input(LOWER_BOUND, UPPER_BOUND)

    while response != LOWER_BOUND:
        if response == 1:
            scan_local()

        elif response == 2:
            port_list = get_ports()

            if port_list is None:
                print("\n\n>>> [ENTER] to return to the menu...")
                input()
            else:
                print_ports(port_list, LOCALHOST)
    
        elif response == 3:
            # if platform.system() == "Windows":
            #     os_warning("Windows")
            # else:
                scan_for_hosts()

        elif response == 4:
            if platform.system() == "Windows":
                os_warning("Windows")
            else:
                ip = None
                while ip is None:
                    print(">>> Enter IP ([0] to cancel): ", end="")
                    ip = check_ip()

                if ip == '0':
                    print("\n\n>>> [ENTER] to return to the menu...")
                    input()
                else:
                    port_check = get_yes_no(">>> Scan ports? [Y/n]: ")

                    print(">>> Loading...")
                    lookup_ip(ip, port_check)
            
        print_menu()
        response = get_int_input(LOWER_BOUND, UPPER_BOUND)

    print(">>> Exiting...")
    time.sleep(0.5)

if __name__ == "__main__":
    main()