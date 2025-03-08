#                             Deathen Tool
#                           [#] root@Deathen
#                 Maded By Devil999x and Managed By Demonop0909
# Deathen Tool is a Source Minecraft Pentesting tool Used To Pentest Minecraft servers for free
# This tool should not be redistributed, modified, or renamed without written permission of owner
# If Rules And Regulations Are Broken You may Get a Loss Through Laws
# This Tool Works For Windows, Linux and Mac OS, if mobile use Termux or etc tools.
# Thanks For Reaching us!

import os
import platform
from commands import scanner, help,  server, info

# Clears the console screen
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Clears the console screen except menu
def clear_screen1():
    if platform.system() == "Windows":
        os.system("cls")
        show_menu(user_name)
    else:
        os.system("clear")
        show_menu(user_name)

# Shows the initial banner
def show_banner():
    banner = """
 ██████████   ██████████   █████████   ███████████ █████   █████ ██████████ ██████   █████    ███████████    ███████       ███████    █████      
░░███░░░░███ ░░███░░░░░█  ███░░░░░███ ░█░░░███░░░█░░███   ░░███ ░░███░░░░░█░░██████ ░░███    ░█░░░███░░░█  ███░░░░░███   ███░░░░░███ ░░███       
 ░███   ░░███ ░███  █ ░  ░███    ░███ ░   ░███  ░  ░███    ░███  ░███  █ ░  ░███░███ ░███    ░   ░███  ░  ███     ░░███ ███     ░░███ ░███       
 ░███    ░███ ░██████    ░███████████     ░███     ░███████████  ░██████    ░███░░███░███        ░███    ░███      ░███░███      ░███ ░███       
 ░███    ░███ ░███░░█    ░███░░░░░███     ░███     ░███░░░░░███  ░███░░█    ░███ ░░██████        ░███    ░███      ░███░███      ░███ ░███       
 ░███    ███  ░███ ░   █ ░███    ░███     ░███     ░███    ░███  ░███ ░   █ ░███  ░░█████        ░███    ░░░░░███████░   ░░░░░░███████░   ███████████
    """
    print(banner)
    input("Click Enter To Continue...")
    clear_screen()

# Displays the main menu
def show_menu(user_name):
    menu = f"""
    =============================================================
    |  # Deathen Tool                   # root@deathen          |
    |                Developed by Devil999x                     |
    =============================================================
    | User Information               | Owner Information        |
    | -----------------------        | ----------------------   |
    | User Name: {user_name}         | Administrator - Devil999x|
    |                                | Manager - Demonop0909    |
    | User Status: Administrator     | Discord: link_here       |
    =============================================================
    """
    print(menu)

# Gets the system username
def get_user_name():
    global user_name
    user_name = os.getlogin()

# Command handler for user inputs
def command_handler(command):
    if not command.strip():
        print("[#] Please type a command to execute.")
        return
    parts = command.split()
    cmd = parts[0].lower()

    if cmd == "help":
        help.show_help()
    elif cmd == "scan":
        scanner.scan(parts)
    elif cmd == "info":
        info.info(parts)
    elif cmd == "server":
        server.handle_mcinfo(parts[1:])
    elif cmd == "bot":  # New Bot Command
        bot.start_bot(parts)
    elif cmd == "clear":
        clear_screen1()
    elif cmd == "exit":
        print("Exiting Deathen Tool...")
        exit()
    else:
        print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")

def main():
    try:
        show_banner()  # Show banner at the beginning
        clear_screen()  # Clear the screen
        user_name = get_user_name()  # Get the system's username
        show_menu(user_name)  # Show the main menu
        
        while True:
            try:
                command = input("[#] root@deathen ➜  ")
                command_handler(command)
            except KeyboardInterrupt:
                print("\n[#] Use 'exit' to quit the tool.")
    
    except KeyboardInterrupt:
        print("\n[#] Exiting Deathen Tool... Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()

