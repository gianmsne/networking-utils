import subprocess
import socket
import ipaddress
import requests
import platform
import re
from concurrent.futures import ThreadPoolExecutor

def get_local():
    """Cross-platform local IP lookup, shared by scan_local() and get_hostname_via_router()."""
    system = platform.system()

    if system == "Windows":
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except OSError:
            return ""

    elif system == "Darwin":  # macOS
        result = subprocess.run(
            ["ipconfig", "getifaddr", "en0"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    else:  # Linux
        # No reliable single interface name across distros — open a dummy
        # UDP socket to a public IP (no packets actually sent) and read
        # which local address the OS would route it through.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return ""


def scan_local():
    """
    Prompt a shell command to print the host machine IP and wait for input
    """
    print("\nYour machine's ip is ", end="")
    print(get_local())
    print("Press [ENTER] to return to the menu...")
    input()


def get_hostname_via_router(ip, router_ip="192.168.0.1"):
    """
        Get the hostname from IP
        (Forces the reverse lookup to go through the 
        router instead of relying on system default DNS)
    """
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["ping", "-a", "-n", "1", "-w", "1000", str(ip)],
                capture_output=True,
                text=True,
                timeout=2
            )

            match = re.search(
                rf"Pinging (.+?) \[{re.escape(str(ip))}\]",
                result.stdout
            )

            if not match:
                return None

            hostname = match.group(1).strip().removesuffix(".modem")

            if ip == get_local():
                hostname += " (Your Device)"

            return hostname
        
        else:
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

    if platform.system() == "Windows":
        result = subprocess.run(
            ["arp", "-a", str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        
    else:
        result = subprocess.run(
            ["arp", "-n", str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )

    if result.returncode == 0:
        if platform.system() == "Windows":
            match = re.search(r"(([0-9a-fA-F]{1,2}-){5}[0-9a-fA-F]{1,2})", result.stdout)
            if match:
                return match.group(0).replace("-", ":")
        else:
            match = re.search(r"(([0-9a-fA-F]{1,2}:){5}[0-9a-fA-F]{1,2})", result.stdout)
            if match:
                return match.group(0)

    return None


def get_latency(ip):
    system = platform.system()

    if system == "Windows":
        result = subprocess.run(
            ["ping", "-n", "5", "-w", "5000", str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
    elif system == "Darwin":  # macOS
        result = subprocess.run(
            ["ping", "-c", "5", "-W", "5000", str(ip)],  # ms on macOS
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
    else:  # Linux
        result = subprocess.run(
            ["ping", "-c", "5", "-W", "5", str(ip)],  # seconds on Linux
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )

    if result.returncode == 0:
        if system == "Windows":
            match = re.search(r"Average = (\d+)ms", result.stdout)
        elif system == "Darwin":
            match = re.search(
                r"round-trip min/avg/max/stddev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms",
                result.stdout
            )
        else:  # Linux
            match = re.search(
                r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms",
                result.stdout
            )

        if match:
            return match.group(1)

    return None


def scan(ip):
    """
        Scan for available devices
        Pings once, waiting 1s for a response.
    """

    system = platform.system()

    if system == "Windows":
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", str(ip)],  # -w in ms
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    elif system == "Darwin":  # macOS
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1000", str(ip)],  # -W in ms
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:  # Linux
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],  # -W in seconds
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    if result.returncode == 0:
        return str(ip)
        # print(ip)
    return None


def get_vendor(mac):
    
    response = requests.get(f"https://api.macvendors.com/{mac}")

    if response.status_code == 200:

        return response.text.strip()

    return "Unknown / locally administered"


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