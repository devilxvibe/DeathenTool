from mcstatus import JavaServer

def fetch_mc_info(server_address):
    try:
        # Connect to the server
        server = JavaServer.lookup(server_address)
        
        # Get basic status
        status = server.status()

        print("\n[#] Fetching Minecraft Server Info...")
        print(f"[#] Server Address: {server_address}")
        print(f"[#] Ping: {status.latency:.2f} ms")

        # Handle MOTD properly (Some servers return it as a string, some as a dictionary)
        motd = status.description
        if isinstance(motd, dict):
            motd_text = motd.get("text", "Unknown MOTD")  # Extract text if dictionary
        else:
            motd_text = str(motd)  # Convert to string if it's not a dictionary
        print(f"[#] MOTD: {motd_text}")

        print(f"[#] Version: {status.version.name} (Protocol: {status.version.protocol})")
        print(f"[#] Players Online: {status.players.online}/{status.players.max}")

        # Get online player names (if available)
        try:
            if status.players.sample:
               print("\n[#] Online Players:")
               for player in status.players.sample:
                print(f"   - {player.name}")  # Display only player names
               else:
                   print("Can't Fetch Players Name")
        except:
            print("Can't Fetch Players Name")

        # Try to get server software & version + plugins
        try:
            query = server.query()
            # Check for plugins
            if query.software.plugins:
                print("\n[#] Installed Plugins:")
                for plugin in query.software.plugins:
                    print(f"   - {plugin}")  # List plugins
        except:
            print("\n[#]No Plugins Detected")

    except Exception as e:
        print(f"[#] Error fetching server info: {e}")

# Function to run from main.py
def handle_mcinfo(args):
    if len(args) < 1:
        print("Usage: mcinfo [server_address]")
        return
    
    server_ip = args[0]
    fetch_mc_info(server_ip)

# Function Completed