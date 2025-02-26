import os
import sys
import socket
import platform
import threading
import subprocess
import time
from mcstatus import JavaServer

def get_ip(target):
    """ Convert a hostname to an IP address. """
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[#] ERROR: Failed to resolve {target} to an IP address.")
        sys.exit(1)

def update_progress(scanned_ports, total_ports):
    """ Display a real-time progress bar. """
    progress = (scanned_ports / total_ports) * 100
    bar_length = 50
    filled_length = int(bar_length * scanned_ports // total_ports)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f"\r[{bar}] {progress:.2f}% Scanned Ports: {scanned_ports}/{total_ports}")
    sys.stdout.flush()

def scan(parts):
    if len(parts) != 4:
        print("[#] Usage: scan [ServerIP] [Port Range] [Method (nmap/masscan/socket)]")
        return

    target = parts[1]
    port_range = parts[2]
    method = parts[3].lower()

    start_port, end_port = map(int, port_range.split("-"))
    total_ports = end_port - start_port + 1

    print(f"\n[#] Scanning {target} on port range {port_range} using {method}...\n")

    if method == "nmap":
        scan_nmap(target, start_port, end_port, total_ports)
    elif method == "masscan":
        scan_masscan(target, start_port, end_port, total_ports)
    elif method == "socket":
        scan_socket(target, start_port, end_port, total_ports)
    else:
        print("[#] Invalid method. Use 'nmap', 'masscan', or 'socket'.")

### ✅ **Nmap Scanner (Real-Time Output)**
def scan_nmap(target, start_port, end_port, total_ports):
    output_file = "nmap_results.txt"
    target_ip = get_ip(target)

    print(f"[#] Starting Nmap scan on {target_ip} from port {start_port} to {end_port}...\n")

    nmap_cmd = f"nmap -p {start_port}-{end_port} --open -oG {output_file} {target_ip}"
    process = subprocess.Popen(nmap_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    scanned_ports = 0
    open_ports = []

    while process.poll() is None:
        if os.path.exists(output_file):
            with open(output_file, "r") as file:
                for line in file:
                    if "/open/" in line:
                        port = int(line.split()[1].split("/")[0])
                        if port not in open_ports:
                            open_ports.append(port)
                    scanned_ports += 1
                    update_progress(scanned_ports, total_ports)
        time.sleep(0.5)

    print("\n\n[#] Scan Complete.\n")
    display_minecraft_servers(target_ip, open_ports)

### ✅ **Masscan Scanner (Real-Time Progress Bar)**
def scan_masscan(target, start_port, end_port, total_ports):
    output_file = "masscan_results.txt"
    target_ip = get_ip(target)

    print(f"[#] Scanning {target} ({target_ip}) on port range {start_port}-{end_port} using Masscan...\n")

    if platform.system() == "Windows":
        masscan_cmd = f"masscan -p{start_port}-{end_port} {target_ip} --rate=500 -oL {output_file}"
    else:
        masscan_cmd = f"sudo masscan -p{start_port}-{end_port} {target_ip} --rate=500 -oL {output_file}"

    process = subprocess.Popen(masscan_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    scanned_ports = 0
    while True:
        output = process.stdout.readline()
        if not output:
            break  

        if "Discovered open port" in output:
            scanned_ports += 1
            update_progress(scanned_ports, total_ports)

    process.wait()
    time.sleep(2)

    if not os.path.exists(output_file) or os.stat(output_file).st_size == 0:
        print("\n[#] No open ports found.\n")
        return

    open_ports = []
    with open(output_file, "r") as file:
        for line in file:
            if "open tcp" in line:
                try:
                    port = int(line.split()[2])
                    if port not in open_ports:
                        open_ports.append(port)
                except (IndexError, ValueError):
                    continue

    print("\n\n[#] Scan Complete.\n")
    display_minecraft_servers(target_ip, open_ports)

### ✅ **Socket Scanner (Threaded)**
def scan_socket(target, start_port, end_port, total_ports):
    open_ports = []
    scanned_ports = 0

    def scan_port(port):
        nonlocal scanned_ports
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            s.close()

            with threading.Lock():
                scanned_ports += 1
                update_progress(scanned_ports, total_ports)

                if result == 0:
                    open_ports.append(port)

        except Exception:
            pass

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()
        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    print("\n\n[#] Scan Complete.\n")
    display_minecraft_servers(target, open_ports)

### ✅ **Show Only Minecraft Servers**
def display_minecraft_servers(target, open_ports):
    """ Show only Minecraft servers with details. """
    minecraft_servers = []
    
    for port in open_ports:
        try:
            server = JavaServer.lookup(f"{target}:{port}")
            status = server.status()
            server_info = {
                "port": port,
                "motd": status.description,
                "version": status.version.name,
                "players": f"{status.players.online}/{status.players.max}",
                "latency": f"{status.latency} ms"
            }
            minecraft_servers.append(server_info)

        except Exception:
            pass  

    if not minecraft_servers:
        print("[#] No Minecraft servers found.\n")
    else:
        print("\n[#] 🎮 **Minecraft Servers Found:**")
        for server in minecraft_servers:
            print(f"🔹 **Port {server['port']}**")
            print(f"   🏷 **MOTD:** {server['motd']}")
            print(f"   🕹 **Version:** {server['version']}")
            print(f"   👥 **Players:** {server['players']}")
            print(f"   ⚡ **Latency:** {server['latency']}\n")

# Function Completed