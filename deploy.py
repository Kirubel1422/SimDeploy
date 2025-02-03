from colorama import Fore
import subprocess
import shlex
import re

# Function to check system requirements before deployment
def check_sys_requirements():
    # Function to check if nginx is installed
    def check_nginx():
        try:
            # Run nginx version command and capture output
            output = subprocess.check_output(shlex.split("nginx -v"), stderr=subprocess.STDOUT).decode()
            version = output.split("/")[1]  # Extract nginx version
            print(Fore.MAGENTA + f"[*] Detected nginx - {version}")
        except FileNotFoundError as e:
            print(Fore.RED + '[!] Nginx not installed in the system: try sudo apt install nginx')
            exit(0)  # Exit if nginx is not found

    # Function to check and enable UFW (firewall)
    def check_ufw():
        try:
            output = subprocess.check_output(shlex.split("ufw status"), stderr=subprocess.STDOUT).decode()
            if "inactive" in output.lower():  # If UFW is inactive
                status = output.split(": ")[1]
                print(Fore.RED + f"[-] UFW status - {status}")

                # Enable UFW for Nginx HTTP and HTTPS
                print(Fore.MAGENTA + "[*] Activating ...")
                cmd = subprocess.check_output(shlex.split("ufw allow 'Nginx HTTP'\\ufw allow 'nginx HTTPS'"), stderr=subprocess.STDOUT).decode()
                print(Fore.GREEN + "[+] UFW enabled successfullly")

            elif "active" in output.lower():  # If UFW is active
                status = output.split(": ")[1]
                print(Fore.GREEN + f"[+] UFW status - {status}")
        except FileNotFoundError as e:
            print(Fore.RED + f'[!] ufw not installed in the system: try sudo apt install ufw')
            exit(0)
    
    # Call both checks
    check_nginx()
    check_ufw()

# Function to test Nginx configuration validity
def test_nginx():
    print(Fore.MAGENTA + '[*] Testing if configuration is successful...')
    try:
        output = subprocess.check_output(shlex.split('nginx -t')).decode()
        if "test is successful" in output:
            print(Fore.GREEN + '[+] Nginx configuration test passed.')
    except Exception as e:
        print(Fore.RED + f'[!] Error occurred while testing nginx conf: {e}')
        exit(0)

# Function to create a symbolic link in Nginx sites-enabled directory
def create_symb_link(project_name):
    try:
        print(Fore.MAGENTA + '[*] Creating symbolic link...')
        subprocess.check_output(shlex.split(f'ln -s /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled/'))
        print(Fore.GREEN + '[+] Symbolic link has been created')
    except Exception as e:
        print(Fore.RED + f'[!] Error occurred while creating symbolic link: {e}')
        exit(0)

# Function to restart Nginx after configuration changes
def restart_nginx():
    try:
        print(Fore.MAGENTA + '[*] Restarting nginx...')
        subprocess.check_output(shlex.split(f'systemctl restart nginx'))
        print(Fore.GREEN + '[+] Nginx has been restarted successfully!')
    except Exception as e:
        print(Fore.RED + f'[!] Error occurred while restarting nginx: {e}')
        exit(0)

# Function to handle SSL certificate generation using Certbot
def handle_ssl(domain_name:str, build_directory:str):
    try:
        print(Fore.MAGENTA + '[*] Checking if certbot exists...')
        subprocess.check_output(shlex.split('certbot -v'))
        print(Fore.GREEN + "[+] Certbot found ...")

        output = subprocess.check_output(shlex.split(f"certbot --nginx -d {domain_name}"), stderr=subprocess.STDOUT)
        print(Fore.GREEN + output)
    except Exception as e:
        print(Fore.RED + f'[!] Failed obtaining SSL certificate: {e}')
        exit(0)

# Main function to automate deployment
def main():
    check_sys_requirements()  # Ensure necessary software is installed
    
    project_name = input('> Project Name: (no spaces or numerics) ')
    path = None

    if not re.match(r'^[a-zA-Z0-9_-]+$', project_name):
        print(Fore.RED + '[!] Project name can only contain letters, numbers, underscores, and hyphens.')
        exit(0)
    
    # Get server name
    server_name = input('> Server name: (www.example.com) ')

    # Get build directory path
    build_directory = input('> Build Directory: (/var/www/demo/dist) ')

    # Read template file and customize it with user input
    file_content = None
    with open("template.txt", 'r') as f:
        file_content = f.read()
    
    file_content = file_content.replace('<build_directory>', build_directory)
    file_content = file_content.replace('<server_name>', server_name)
    
    # Write the updated configuration file to Nginx's sites-available directory
    with open(f'/etc/nginx/sites-available/{project_name}', "w") as f:
        f.write(file_content)
    
    # Test the new Nginx configuration
    test_nginx()

    # Create symbolic link to enable site
    create_symb_link(project_name)

    # Restart nginx to apply changes
    restart_nginx()
    
    # Ask user if they want to enable SSL
    ssl_flag = input("> Do you want to get SSL certificate? [Y/n] ")
    if 'y' == ssl_flag.lower():
        handle_ssl(server_name, build_directory)
    else:
        print('Bye!')

if __name__ == "__main__":
    welcome_text = r"""
        _________.__        ________                .__                
    /   _____/|__| _____ \______ \   ____ ______ |  |   ____ ___.__.
    \_____  \ |  |/     \ |    |  \_/ __ \\____ \|  |  /  _ <   |  |
    /        \|  |  Y Y  \|    `   \  ___/|  |_> >  |_(  <_> )___  |
    /_______  /|__|__|_|  /_______  /\___  >   __/|____/\____// ____|
            \/          \/        \/     \/|__|               \/   
    
    Welcome to SimDeploy
    Made by [Kirubel Mamo]
    Github Kirubel1422
    ----------------------------------------------------------------
    """
    print(Fore.GREEN + welcome_text + "\n\n")
    
    main()
