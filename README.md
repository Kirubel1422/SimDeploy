# SimDeploy - Automated Nginx Configuration Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/Kirubel1422/SimDeploy.svg)](https://github.com/Kirubel1422/SimDeploy/issues)
[![GitHub forks](https://img.shields.io/github/forks/Kirubel1422/SimDeploy.svg)](https://github.com/Kirubel1422/SimDeploy/network)
[![GitHub stars](https://img.shields.io/github/stars/Kirubel1422/SimDeploy.svg)](https://github.com/Kirubel1422/SimDeploy/stargazers)

SimDeploy is a Python-based tool designed to automate the Nginx configuration process for your web projects. It ensures the necessary system requirements are met, configures Nginx for your project, creates symbolic links, restarts Nginx, and optionally sets up SSL certificates using Certbot.

## Features ✨

- **Test Nginx Configuration**: Validates Nginx configuration.
- **Symbolic Link Creation**: Automatically creates a symbolic link to enable your site's configuration.
- **Restart Nginx**: Restarts Nginx to apply configuration changes.
- **SSL Certificate Setup**: Optionally sets up SSL certificates with Certbot for secure HTTPS. 🔒

## Requirements

Before using SimDeploy, ensure that the following software is installed on your system:

- **Nginx**: The tool checks if Nginx is installed and runs the necessary commands to configure it.

  - Install Nginx:
    ```bash
    sudo apt install nginx
    ```

- **UFW (Uncomplicated Firewall)**: SimDeploy will configure your firewall for Nginx HTTP/HTTPS if not already active.

  - Install UFW:
    ```bash
    sudo apt install ufw
    ```

- **Certbot (for SSL certificates)**: If you want to enable SSL, Certbot will be required.
  - Install Certbot:
    ```bash
    sudo apt install certbot python3-certbot-nginx
    ```

## Installation

**Clone this repository:**

```bash
 # Clone repository
 git clone https://github.com/Kirubel1422/SimDeploy.git

 # Install dependencies
 pip install -r requirements.txt

 # (Recommended) Use virtual environment
 python -m venv venv
 source venv/bin/activate  # Linux/Mac
 venv\Scripts\activate  # Windows
```

## Usage 🚀

### Basic Command

```bash
sudo python3 deploy.py
```

## Contributing 🤝

- Fork the repository
- Create feature branch: git checkout -b feat/new-feature
- Commit changes: git commit -m 'Add awesome feature'
- Push to branch: git push origin feat/new-feature
- Open pull request
