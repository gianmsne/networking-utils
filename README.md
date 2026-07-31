# Networking Utility Toolkit

A lightweight command-line toolkit for common networking tasks I find myself needing while learning and working with computer networks.

Built with Python, the project currently provides utilities for discovering local network information, identifying devices on a LAN, and inspecting open ports on the local machine. Currently, it is only a command-line application.

*This project is a work in progress that I intend to iterate on and expand over time.*

## Features

### Local IP Information
Retrieves the local IP address assigned to the host machine.
```
Your machine's IP is 192.168.x.x
````

### Local Port Scanner
Scans the local machine for open TCP ports. It checks the full TCP port range 1 - 65,535 or a specified port range and reports any ports accepting connections.
For port ranges <= 20, it will display both closed and open ports.
```
Scanning for open ports on your device.

Port 22 is open
Port 80 is open
Port 631 is open
```

### Local Network Discovery

Scan the local network for active devices. The scanner:

* Checks each host for availability
* Uses concurrent threads to speed up network discovery
* Resolves discovered IP addresses to hostnames where possible
* Displays a simple summary of discovered devices

Example:
```
Searching for devices on your local network...
      IP              Hostname
-----------------------------------
192.168.0.1       router
192.168.0.42      my-computer
192.168.0.111     raspberrypi

Found 3 devices.
```

## Technologies

* Python
* **socket:** TCP connections and network communication
* **ipaddress:** IP address and network manipulation
* **subprocess:** interaction with system networking utilities
* **concurrent.futures:** concurrent network scanning
* **ThreadPoolExecutor:** multi-threaded host discovery


## How It Works

### Host Discovery
The network scanner determines the hosts within the configured local network and concurrently sends ICMP echo requests to each address. A ThreadPoolExecutor is used to check multiple addresses at the same time rather than scanning them sequentially. This is particularly useful because network scanning is largely I/O-bound, with each request spending much of its time waiting for a response.

### Port Scanning
The port scanner attempts to establish TCP connections to ports on the local machine. A successful connection indicates that a service is listening on that port.


## Getting Started

Requirements:

* Python 3.9+
* macOS or another Unix-like operating system (for now)
* Access to the local network

The current implementation uses system networking commands such as ping, nslookup, and ipconfig, so some functionality may require modification for Windows.

Clone the repository:
```
git clone https://github.com/your-username/networking-utils.git
cd networking-utils
```

Create a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

Run the application:
```
python3 main.py
```

## Usage

After launching the application, a menu provides access to the available utilities:
```
------- Menu -------
1. Get local machine IP
2. Scan local machine for open ports
3. Scan local network for devices
4. Exit
*  Enter menu item:
```
Select an option and follow the prompts.


## Configuration

The local network is currently configured as 192.168.0.0/24.

If your network uses a different subnet, update the network definition in the `scan_for_hosts()` method:
```
network = ipaddress.ip_network("192.168.0.0/24", strict=False)
```
The router address used for hostname resolution can also be configured through:
```
get_hostname_via_router(ip, router_ip="192.168.0.1")
```

## Planned Improvements
Some features I’d like to add include:

* Automatic local subnet detection
* Cross-platform support
* Simulated network environments using Docker containers
* Improved port scanning performance
* Better error handling
* A front-end interface


## Project Goals

The primary goal of this project is to build a networking toolkit I can personally use, while developing a deeper understanding of:

* TCP/IP networking
* IP addressing and subnetting
* TCP ports and services
* DNS and reverse DNS
* Network discovery
* Socket Programming
* Multithreading

***

### ⚠️ Disclaimer

This tool is intended for educational purposes and use on networks and devices you own or have permission to test. Network scanning and port scanning can generate significant network traffic and may be detected or blocked by network security systems.
