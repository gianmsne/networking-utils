import subprocess
import time
from unicodedata import numeric
from scanner import scan_local, scan_ports, scan_for_hosts

def print_menu():
    for i in range(10): 
        print("\n") 
        time.sleep(0.01)
    print("----- Network Tool -----")
    print("1. Get local machine IP")
    print("2. Scan local machine for open ports")
    print("3. Scan local network for devices")
    print("4. Exit")
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



def main():

    print_menu()
    response = get_int_input(1, 4)

    while response != 4:

        if response == 1:
            scan_local()

        elif response == 2:
            scan_ports()

        elif response == 3:
            scan_for_hosts()
            
        print_menu()
        response = get_int_input(1, 4)

    print(" Exiting...")
    time.sleep(0.5)

if __name__ == "__main__":
    main()