import socket
import re
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from config import (
    COMMON_PORTS,
    DEFAULT_MAX_WORKERS,
    DEFAULT_TIMEOUT,
    MAX_PORT,
    MIN_PORT,
)

def parse_ports(input_string):
    """
        Split ports into individual list items.
        Handles ranges (e.g. 20-500)
    """

    ports = re.split(r'[,\s]+', input_string)
    port_chunks = []

    for item in ports:
        
        match = re.fullmatch(r"(\d+)-(\d+)", item)

        if match:

            start = int(match.group(1))
            end = int(match.group(2))

            if start > end:
                continue

            port_chunks.extend(range(start, end + 1))
                                     
        elif item.isnumeric():
            port_chunks.append(int(item))

    return port_chunks


def get_ports():
    """
        Request port range from user
    """

    ports = input(
        "\nPort Scan\n"
        "----------------------------------------\n"
        "Enter ports to scan\n"
        "  e.g. 1,5,22,40-1024,8080\n"
        "\n"
        "  [ENTER] Scan all ports (1-65535)\n"
        "----------------------------------------\n"
        "> "
    )
    
    if not ports:
        return parse_ports("1-65535")
    
    return parse_ports(ports)


def scan_ports(port, target, show_closed_ports=None):

    if port < MIN_PORT or port > MAX_PORT:
        print(f"[!] Removed port {port} from list. Must be {MIN_PORT}-{MAX_PORT}")
        return
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(DEFAULT_TIMEOUT)
        result = s.connect_ex((target, port))

    if result == 0:
        if port in COMMON_PORTS:
            print(f"Port {port} is open ({COMMON_PORTS[port]})")
        else:
            print(f"Port {port} is open (?)")
    elif show_closed_ports:
        print(f"Port {port} is closed")
    

def print_ports(port_list, target, show_closed_ports = None):
    """
            Scan specified ports of a target machine
    """

    # Show closed ports if listing less than 20 ports inclusive
    if show_closed_ports is None:
            show_closed_ports = len(port_list) <= 20

    scan = partial(
        scan_ports,
        target=target,
        show_closed_ports=show_closed_ports
    )

    with ThreadPoolExecutor(max_workers=DEFAULT_MAX_WORKERS) as executor:
        list(executor.map(scan, port_list))

    print()
    print(">>> [ENTER] to return to the menu...")
    input()