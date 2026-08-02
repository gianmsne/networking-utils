import time
from tools.scanner import scan_local, scan_for_hosts, scan
from tools.ports import get_ports, scan_ports
from tools.check_ip import lookup_ip
from utils.validation import get_int_input, check_ip

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

# For state machine menu
LOWER_BOUND = 0
UPPER_BOUND = 4

LOCALHOST = "127.0.0.1"

def main():

    print_menu()
    response = get_int_input(LOWER_BOUND, UPPER_BOUND)
    
    while response != LOWER_BOUND:

        if response == 1:
            scan_local()

        elif response == 2:
            port_list = get_ports(LOCALHOST)
            scan_ports(port_list)
    
        elif response == 3:
            scan_for_hosts()

        elif response == 4:
            ip = None
            while ip is None:
                print(">>> Enter IP: ", end="")
                ip = check_ip()
            lookup_ip(ip)
            
        print_menu()
        response = get_int_input(LOWER_BOUND, UPPER_BOUND)

    print(">>> Exiting...")
    time.sleep(0.5)

if __name__ == "__main__":
    main()