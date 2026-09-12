import ipaddress


"""
    Helper Functions    
"""

def is_valid_ip(ip):
    if '/' not in ip:
        return False
    try:
        net = ipaddress.ip_network(ip, strict=False)
        return net.version == 4
    except ValueError:
        return False

def is_integer(value):
    try:
        return 0 < int(value) <= 100
    except (ValueError, TypeError):
        return False

# Helper to convert back from integer to dotted string
def int_to_ip(n):
    return f"{(n >> 24) & 255}.{(n >> 16) & 255}.{(n >> 8) & 255}.{n & 255}"


def subnet_calculator():
    while True:
        address = input(
            "\nSubnet Calculator\n"
            "----------------------------------------\n"
            "Enter the IP address\n"
            "  e.g. 192.168.1.0/24\n"
            "\n"
            "> "
        )
        if is_valid_ip(address):
            break
        print("Invalid IP address, please try again.")


    while True:
        subnets_input = input(
            "\nEnter the number of subnets\n"
            "  e.g. 4\n"
            "\n"
            "> "
        )
        if is_integer(subnets_input):
            subnets = int(subnets_input)
            break
        print("Invalid number, please try again.")


    ### Find how many bits to borrow
    prefix = int(address.split("/", 1)[1])

    count = 0
    while 2**count < subnets:
        count += 1


    ### Calculate new prefix length
    new_prefix = prefix + count
    if new_prefix > 32:
        print("Error: too many subnets requested for this network.")
        exit()

    mask_int = (0xFFFFFFFF << (32 - new_prefix)) & 0xFFFFFFFF
    print(f"New subnet mask: {int_to_ip(mask_int)}")

    #### Calculate remaining host bits and hosts per subnet
    host_bits = 32 - new_prefix
    hosts_per_subnet = 2**host_bits 


    #### Table Printer
    print()
    # Get the base network address (ignore any prefix already on it)
    base_ip = address.split("/", 1)[0]

    # Convert IP string to a single 32-bit integer
    octets = [int(o) for o in base_ip.split(".")]
    ip_int = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]

    headers = ["Subnet #", "Network Address", "First Usable", "Last Usable", "Broadcast Address"]

    rows = []
    for i in range(subnets):
        network_addr = ip_int + (i * hosts_per_subnet)
        broadcast_addr = network_addr + hosts_per_subnet - 1
        first_usable = network_addr + 1
        last_usable = broadcast_addr - 1

        rows.append([
            str(i + 1),
            f"{int_to_ip(network_addr)}/{new_prefix}",
            int_to_ip(first_usable),
            int_to_ip(last_usable),
            int_to_ip(broadcast_addr),
        ])

    # Work out each column's width from the longest cell (header or data)
    widths = [
        max(len(headers[col]), *(len(row[col]) for row in rows))
        for col in range(len(headers))
    ]

    def format_row(cells):
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)) + " |"

    separator = "|-" + "-|-".join("-" * w for w in widths) + "-|"

    print()
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))

subnet_calculator()