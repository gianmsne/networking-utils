import subprocess
import ipaddress
import re
from concurrent.futures import ThreadPoolExecutor

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

def get_mac_address(ip):

    result = subprocess.run(
        ["arp", "-n", str(ip)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    
    if result.returncode == 0:
        match = re.search(r"(([0-9a-fA-F]{1,2}:){5}[0-9a-fA-F]{1,2})", result.stdout)
        if match:
            return match.group(0)

    return None


def scan(ip):
    """
        Scan for available devices
        Pings once, waiting 1s for a response.
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

    print(">>> [ENTER] to return to the menu...")
    input()