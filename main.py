import time
from scanner import scan_local, scan_ports, scan_for_hosts

def print_menu():
    for _ in range(10): 
        print("\n") 
        time.sleep(0.01)
    print("----- Network Tool -----")
    print("1. Get local machine IP")
    print("2. Scan local machine for open ports")
    print("3. Scan local network for devices")
    print("0. Exit")
    print("\n*  Enter menu item: ", end="")


def get_int_input(lower_bound, upper_bound):
    try:
        response = int(input())
    except ValueError:
        print("\nPlease enter a number")
        time.sleep(1)
        return

    if not lower_bound <= response <= upper_bound:
        print(f"\nEnter a number between {lower_bound} and {upper_bound}")
        time.sleep(1)
        return

    return response

# For state machine menu
LOWER_BOUND = 0
UPPER_BOUND = 3

def main():

    print_menu()
    response = get_int_input(LOWER_BOUND, UPPER_BOUND)

    while response != LOWER_BOUND:

        if response == 1:
            scan_local()

        elif response == 2:
            scan_ports()
    
        elif response == 3:
            scan_for_hosts()
            
        print_menu()
        response = get_int_input(LOWER_BOUND, UPPER_BOUND)

    print(" Exiting...")
    time.sleep(0.5)

if __name__ == "__main__":
    main()