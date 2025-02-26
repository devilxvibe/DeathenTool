import socket
import requests
import time

def get_ip(target):
    """ Convert a hostname to an IP address. """
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[#] ERROR: Failed to resolve {target} to an IP address.")
        return None

def get_ping(target_ip):
    """ Measure the server's ping (latency) in milliseconds. """
    try:
        ping_start = time.time()
        socket.create_connection((target_ip, 80), timeout=1)
        ping_end = time.time()
        return round((ping_end - ping_start) * 1000, 2)  # Convert to ms
    except Exception:
        return "N/A"

def info(parts):
    """ Fetch server geolocation, ISP, and ping details. """
    if len(parts) != 2:
        print("[#] Usage: info [Server IP/Domain]")
        return

    target = parts[1]
    target_ip = get_ip(target)
    if not target_ip:
        return

    try:
        # Get Geolocation Info
        response = requests.get(f"http://ip-api.com/json/{target_ip}").json()
        country = response.get("country", "Unknown")
        region = response.get("regionName", "Unknown")
        city = response.get("city", "Unknown")
        isp = response.get("isp", "Unknown")
        latitude = response.get("lat", "N/A")
        longitude = response.get("lon", "N/A")

        # Get Ping (Latency)
        latency = get_ping(target_ip)

        # Display Info
        print(f"\n[#] Server Information for {target} ({target_ip}):")
        print(f"[#] **Country:** {country}")
        print(f"[#] **Region:** {region}, {city}")
        print(f"[#] **ISP:** {isp}")
        print(f"[#] **Location:** {latitude}, {longitude}")
        print(f"[#] **Ping:** {latency} ms\n")

    except Exception as e:
        print("[#] ERROR: Unable to fetch server info.")
        print(str(e))
