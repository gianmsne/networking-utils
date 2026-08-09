from utils.validation import check_ip
from tools.scanner import get_hostname_via_router, scan, get_mac_address, get_latency, get_vendor
from tools.ports import scan_ports, split_ports

def lookup_ip(ip):
    
    hostname = get_hostname_via_router(ip)
    port_list = split_ports("1-65535")
    mac_address = get_mac_address(ip)
    vendor = get_vendor(mac_address)
    latency = get_latency(ip)

    print("\n\n\n")
    print(f"===== Device: {ip} =====")

    print("\n--- Host Information ---")
    print(f"IP Address: {ip}")
    print(f"Hostname: {hostname}")
    print(f"MAC Address: {mac_address}")
    print(f"Vendor: {vendor}")

    print("\n--- Network ---")
    print("Status: ", end="") 
    if scan(ip): 
        print("Reachable")
        print(f"Latency: {latency}ms")
    else:
        print("Unavailable")

    print("\n--- Open Ports ---", end="")
    scan_ports(port_list, ip, show_closed_ports=False)
    