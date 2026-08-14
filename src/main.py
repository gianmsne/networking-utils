import time
from tools.scanner import scan_local, scan_for_hosts
from tools.ports import get_ports, print_ports
from tools.check_ip import lookup_ip
from utils.validation import get_int_input, check_ip, get_yes_no
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
            print_ports(port_list, LOCALHOST)
    
        elif response == 3:
            scan_for_hosts()

        elif response == 4:
            ip = None
            while ip is None:
                print(">>> Enter IP: ", end="")
                ip = check_ip()

            port_check = get_yes_no(">>> Scan ports? [Y/n]: ")

            print(">>> Loading...")
            lookup_ip(ip, port_check)
            
        print_menu()
        response = get_int_input(LOWER_BOUND, UPPER_BOUND)

    print(">>> Exiting...")
    time.sleep(0.5)

if __name__ == "__main__":
    main()