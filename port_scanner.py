import socket
import time
import sys
from datetime import datetime


def scan_ports():
    target = "127.0.0.1"
    print("\nScanning for open ports on your device!\n")
    time.sleep(0.5)
    try:
        
        for port in range(1,65535):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)

                result = s.connect_ex((target,port))
                if result == 0:
                        print(f"Port {port} is open")
                s.close()
    except KeyboardInterrupt:
        print("\nExiting Program.")
        sys.exit()
    except socket.gaierror:
        print("\nHostname Could Not Be Resolved.")
        sys.exit()
    except socket.error:
        print("\nServer not responding.")
        sys.exit()

    print("Press [ENTER] to return to the menu...")
    input()
