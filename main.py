import subprocess
import time
from unicodedata import numeric
from port_scanner import scan_ports

def print_menu():
    for i in range(10): 
        print("\n") 
        time.sleep(0.01)
    print("----- Network Tool -----")
    print("1. Get local machine IP")
    print("2. Scan local machine open ports")
    print("3. Exit")
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



def get_local():
    print("\nYour machine's ip is ", end="")
    subprocess.run('ipconfig getifaddr en0', shell=True)
    print("Press [ENTER] to return to the menu...")
    input()



def main():

    print_menu()
    response = get_int_input(1, 3)

    while response != 3:

        if response == 1:
            get_local()

        elif response == 2:
            scan_ports()
            
        print_menu()
        response = get_int_input(1, 3)

    print(" Exiting...")
    time.sleep(0.5)

if __name__ == "__main__":
    main()