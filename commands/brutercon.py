import time
import random

def brutercon(parts):
    if len(parts) != 4:
        print("[#] Usage: brutercon [host] [port] [password list]")
        return
    host = parts[1]
    port = int(parts[2])
    password_list = parts[3]

    print(f"[#] Brute-forcing RCON on {host}:{port} with passwords from {password_list}")
    with open(password_list, "r") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()
        print(f"[#] Trying password: {password}")
        # Implement actual RCON brute force logic here (using `mcrcon` or similar)
        time.sleep(random.uniform(0.5, 2.0))
        # If successful, break
