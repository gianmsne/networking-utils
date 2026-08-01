import time
import socket
import sys
import re

# https://www.iana.org/assignments/service-names-port-numbers
COMMON_PORTS = {
    20 : "FTP Data",
    21 : "FTP",
    22 : "SSH",
    23: "Telnet",
    25 : "SMTP",
    53 : "DNS",
    80 : "HTTP",
    110: "POP3",
    123 : "NTP",  # https://datatracker.ietf.org/doc/html/rfc5905
    143: "IMAP",
    443 : "HTTPS",
    500 : "ISAKMP",
    587 : "SMTP",
    631: "IPP [Printing]",
    3306: "MySQL",
    3389 : "RDP",  # https://www.cloudflare.com/learning/access-management/what-is-the-remote-desktop-protocol/
    5432: "PostgreSQL",
    6379: "Redis",
    6463: "Discord Rich Presence",
    7265: "Raycast Web Socket",
    8080: "HTTP Proxy",
    33060: "MySQL Extended UI"
}


def split_ports(input_string):
    """
        Split ports into individual list items.
        Handles ranges (e.g. 20-500)
    """

    ports = re.split(r'[,\s]+', input_string)
    port_chunks = []

    for item in ports:
        
        match = re.fullmatch(r"(\d+)-(\d+)", item)

        if match:

            start_var = match.group(1)
            end_var = match.group(2)

            if not start_var.isnumeric() or not end_var.isnumeric():
                continue
            
            start = int(start_var)
            end = int(end_var)

            port_chunks.extend(range(start, end + 1))
                                     
        elif item.isnumeric():
            port_chunks.append(int(item))

    return port_chunks


def scan_ports():
    """
        Scan for open ports on local machine
    """
    target = "127.0.0.1"
    port_list = []
    short_list = False

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
        port_list += split_ports("1-65535")
    else:
        port_list += split_ports(ports)

    # Show closed ports if listing less than 20 ports inclusive
    short_list = True if len(port_list) <= 20 else False 

    print()
    try:
        
        for port in port_list:
            
            if port < 1 or port > 65535:
                port_list.remove(port)
                print(f"[!] Removed port {port} from list. Must be 1-65535")
                continue
                

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            result = s.connect_ex((target,port))
            if result == 0:
                    if port in COMMON_PORTS:
                         print(f"Port {port} is open ({COMMON_PORTS[port]})")
                    else:
                         print(f"Port {port} is open (?)")
            elif short_list:
                    print(f"Port {port} is closed")
            s.close()
        print()
    
    except KeyboardInterrupt:
        print("\nExiting Program.")
        sys.exit()
    except socket.gaierror:
        print("\nHostname Could Not Be Resolved.")
        sys.exit()
    except socket.error:
        print("\nServer not responding.")
        sys.exit()

    print(">>> [ENTER] to return to the menu...")
    input()