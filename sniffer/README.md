# WiFi Sniffer Installation Guide

This directory contains a complete installation script for setting up the WiFi Sniffer as a system service on Linux machines.

## Quick Start

To install the WiFi Sniffer on a Linux machine, run the following command from this directory:

```bash
sudo bash install_sniffer.sh
```

## What the Installation Script Does

The `install_sniffer.sh` script automates the entire setup process:

### 1. **System Dependencies**
- Updates package lists
- Installs Python3, pip, and venv
- Installs curl for health checks

### 2. **Application Setup**
- Creates installation directory at `/home/test/Sniffer`
- Copies all application files
- Sets proper file permissions

### 3. **Python Environment**
- Creates a virtual environment
- Installs required packages: `flask` and `pyserial`

### 4. **Serial Port Permissions**
- Creates udev rules for persistent serial port permissions
- Sets permissions for `/dev/ttyUSB0` and `/dev/ttyACM*` devices
- Adds user to `dialout` group for serial access

### 5. **System Service**
- Creates a systemd service file
- Enables automatic startup on boot
- Configures proper user permissions and restart policies

### 6. **Management Tools**
- Creates convenient management scripts:
  - `status_sniffer.sh` - Check service status
  - `logs_sniffer.sh` - View service logs
  - `restart_sniffer.sh` - Restart the service
  - `start_sniffer.sh` - Start the service
  - `stop_sniffer.sh` - Stop the service
  - `uninstall_sniffer.sh` - Complete uninstallation

## Manual Installation (Alternative)

If you prefer to install manually, follow these steps:

### 1. Install Dependencies
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

### 2. Setup Application
```bash
sudo mkdir -p /home/test/Sniffer
sudo cp -r ./* /home/test/Sniffer/
sudo chown -R $(whoami):$(whoami) /home/test/Sniffer
cd /home/test/Sniffer
python3 -m venv venv
source venv/bin/activate
pip install flask pyserial
deactivate
```

### 3. Setup Serial Permissions
```bash
sudo tee /etc/udev/rules.d/99-usb-serial.rules > /dev/null << EOF
KERNEL=="ttyUSB[0-9]*", MODE="0666", GROUP="dialout"
KERNEL=="ttyACM[0-9]*", MODE="0666", GROUP="dialout"
EOF
sudo udevadm control --reload-rules
```

### 4. Create Service
```bash
sudo tee /etc/systemd/system/sniffer.service > /dev/null << EOF
[Unit]
Description=WiFi Sniffer Flask Application
After=network.target
RequiresMountsFor=/home/test/Sniffer

[Service]
Type=simple
User=$(whoami)
Group=$(whoami)
WorkingDirectory=/home/test/Sniffer
Environment=PATH=/home/test/Sniffer/venv/bin
ExecStart=/home/test/Sniffer/venv/bin/python /home/test/Sniffer/app.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
SyslogIdentifier=sniffer
SupplementaryGroups=dialout

[Install]
WantedBy=multi-user.target
EOF
```

### 5. Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable sniffer
sudo systemctl start sniffer
sudo systemctl status sniffer
```

## Usage

After installation:

1. **Access the Web Interface**: Open your browser and go to `http://localhost:5000`

2. **Check Service Status**:
   ```bash
   sudo systemctl status sniffer
   ```

3. **View Logs**:
   ```bash
   sudo journalctl -u sniffer -f
   ```

4. **Restart Service**:
   ```bash
   sudo systemctl restart sniffer
   ```

## Management Scripts

After installation, you'll find these convenient scripts in `/home/test/Sniffer/`:

- `status_sniffer.sh` - Check service status and recent logs
- `logs_sniffer.sh` - View the last 50 lines of service logs
- `restart_sniffer.sh` - Restart the service
- `start_sniffer.sh` - Start the service
- `stop_sniffer.sh` - Stop the service
- `uninstall_sniffer.sh` - Complete uninstallation

## Troubleshooting

### Serial Port Permission Issues
If you get permission errors with the serial port:
```bash
# Check if device is connected
ls -la /dev/ttyUSB*

# Check current permissions
ls -la /dev/ttyUSB0

# Manually set permissions (temporary)
sudo chmod 666 /dev/ttyUSB0

# Add user to dialout group (permanent)
sudo usermod -a -G dialout $(whoami)
```

### Service Not Starting
Check the service status and logs:
```bash
sudo systemctl status sniffer
sudo journalctl -u sniffer --no-pager -l
```

### Python Dependencies
If you get import errors, reinstall dependencies:
```bash
cd /home/test/Sniffer
source venv/bin/activate
pip install flask pyserial
deactivate
```

## Uninstallation

To completely remove the WiFi Sniffer:

```bash
sudo /home/test/Sniffer/uninstall_sniffer.sh
```

Or manually:
```bash
sudo systemctl stop sniffer
sudo systemctl disable sniffer
sudo rm -f /etc/systemd/system/sniffer.service
sudo rm -f /etc/udev/rules.d/99-usb-serial.rules
sudo systemctl daemon-reload
sudo udevadm control --reload-rules
```

## Security Notes

- The service runs as a non-root user for security
- The application binds to all interfaces (0.0.0.0:5000)
- Consider using a firewall to restrict access if needed
- Serial port permissions are set to 666 (read/write for all)

## Requirements

- Linux system with systemd
- Python 3.6 or higher
- sudo privileges for installation
- USB serial device connected to `/dev/ttyUSB0` or similar