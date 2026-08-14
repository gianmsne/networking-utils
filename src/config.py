# config.py

# Port range
MIN_PORT = 1
MAX_PORT = 65535

# Port scanning
DEFAULT_TIMEOUT = 0.5
DEFAULT_MAX_WORKERS = 200

# https://www.iana.org/assignments/service-names-port-numbers
COMMON_PORTS = {
    20:     "FTP Data",
    21:     "FTP",
    22:     "SSH",
    23:     "Telnet",
    25:     "SMTP",
    53:     "DNS",
    67:     "DHCP Server",
    68:     "DHCP Client",
    80 :    "HTTP",
    110:    "POP3",
    119:    "NNTP",
    123:    "NTP", 
    143:    "IMAP",
    161:    "SNMP",
    194:    "IRC",
    443:    "HTTPS",
    445:    "SMB",
    500:    "ISAKMP",
    587:    "SMTP",
    631:    "IPP [Printing]",
    993:    "IMAPS",
    995:    "POP3S",
    3306:   "MySQL",
    3389:   "RDP", 
    5432:   "PostgreSQL",
    6379:   "Redis",
    6463:   "Discord Rich Presence",
    7265:   "Raycast Web Socket",
    8080:   "HTTP Proxy",
    33060:  "MySQL Extended UI"
}