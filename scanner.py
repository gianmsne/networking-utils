import socket
import time
import sys
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def scan_local():
    """
    Prompt a shell command to print the host machine IP and wait for input
    """
    print("\nYour machine's ip is ", end="")
    subprocess.run('ipconfig getifaddr en0', shell=True)
    print("Press [ENTER] to return to the menu...")
    input()

def get_local():
    """
        Prompt a shell command to get the host machine IP without printing
    """
    local_ip = subprocess.run('ipconfig getifaddr en0', shell=True, capture_output=True, text=True)
    local_ip = local_ip.stdout.strip()
    return local_ip

def scan_ports():
    """
        Scan for open ports on local machine
    """
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


def get_hostname_via_router(ip, router_ip="192.168.0.1"):
    """
        Get the hostname from IP
        (Forces the reverse lookup to go through the 
        router instead of relying on system default DNS)
    """
    try:
        result = subprocess.run(
            ["nslookup", ip, router_ip],
            capture_output=True, text=True, timeout=2
        )
        
        for line in result.stdout.splitlines():
            if "name =" in line:
                hostname = line.split("name =")[1].strip().removesuffix(".modem.")
                if ip == get_local():
                    hostname += " (Your Device)"
                return hostname
    except Exception:
        pass
    return None

def scan(ip):
        """
            Scan for available devices
        """
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return str(ip)
            # print(ip)
        return None

def scan_for_hosts():
    """
    Scans the local /24 network for active hosts using multiple threads,
    then displays each discovered host's IP address and hostname.
    """
    
    network = ipaddress.ip_network("192.168.0.0/24", strict=False)
    found = []

    print("\nSearching for devices on your local network...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(scan, network.hosts())

    found = [ip for ip in results if ip is not None]
    
    print(f"\n{'IP':^13}{'Hostname':>20}")
    for ip in found:
        print(f"{ip:<13} -> {get_hostname_via_router(ip) or '[unknown]'}")
            
    print(f"\nFound {len(found)} devices.")

    print("Press [ENTER] to return to the menu...")
    input()