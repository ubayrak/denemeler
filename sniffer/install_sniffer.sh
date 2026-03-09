#!/bin/bash

# WiFi Sniffer Installation Script
# This script sets up the sniffer tool as a system service with proper serial permissions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="/home/test/Sniffer"
SERVICE_NAME="sniffer"
SERIAL_PORT="/dev/ttyUSB0"
PYTHON_VERSION="python3"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root for security reasons."
        print_status "Please run as a regular user with sudo privileges."
        exit 1
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system dependencies
install_dependencies() {
    print_status "Installing system dependencies..."
    
    # Update package list
    sudo apt update
    
    # Install Python and pip if not present
    if ! command_exists python3; then
        print_status "Installing Python3..."
        sudo apt install -y python3 python3-pip python3-venv
    else
        print_success "Python3 already installed"
    fi
    
    # Install curl for health checks
    if ! command_exists curl; then
        print_status "Installing curl..."
        sudo apt install -y curl
    else
        print_success "curl already installed"
    fi
}

# Function to setup user and directories
setup_directories() {
    print_status "Setting up directories..."
    
    # Create installation directory
    mkdir -p "$INSTALL_DIR"
    
    # Copy application files to installation directory
    print_status "Copying application files to $INSTALL_DIR..."
    cp -r ./* "$INSTALL_DIR/" 2>/dev/null || true
    
    # Set proper ownership
    sudo chown -R $(whoami):$(whoami) "$INSTALL_DIR"
    
    print_success "Directories setup complete"
}

# Function to setup Python environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    cd "$INSTALL_DIR"
    
    # Create virtual environment
    $PYTHON_VERSION -m venv venv
    
    # Activate virtual environment and install dependencies
    source venv/bin/activate
    
    # Install required packages
    pip install flask pyserial
    
    # Deactivate virtual environment
    deactivate
    
    print_success "Python environment setup complete"
}

# Function to setup serial port permissions
setup_serial_permissions() {
    print_status "Setting up serial port permissions..."
    
    # Check if serial port exists
    if [ ! -c "$SERIAL_PORT" ]; then
        print_warning "Serial port $SERIAL_PORT not found. This is normal if no USB device is connected."
        print_status "Serial port permissions will be applied when the device is connected."
    fi
    
    # Create udev rule for persistent serial port permissions
    print_status "Creating udev rule for serial port permissions..."
    
    sudo tee /etc/udev/rules.d/99-usb-serial.rules > /dev/null << EOF
# WiFi Sniffer Serial Port Permissions
KERNEL=="ttyUSB[0-9]*", MODE="0666", GROUP="dialout"
KERNEL=="ttyACM[0-9]*", MODE="0666", GROUP="dialout"
EOF
    
    print_success "Udev rule created. Serial port permissions will be applied on next connection."
    
    # Also set current permissions if device is connected
    if [ -c "$SERIAL_PORT" ]; then
        sudo chmod 666 "$SERIAL_PORT"
        print_success "Current serial port permissions set"
    fi
}

# Function to create systemd service
create_service() {
    print_status "Creating systemd service..."
    
    # Create service file
    sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << EOF
[Unit]
Description=WiFi Sniffer Flask Application
After=network.target
RequiresMountsFor=$INSTALL_DIR

[Service]
Type=simple
User=$(whoami)
Group=$(whoami)
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/venv/bin
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/app.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
SyslogIdentifier=sniffer
SupplementaryGroups=dialout

[Install]
WantedBy=multi-user.target
EOF
    
    print_success "Systemd service created"
}

# Function to enable and start service
start_service() {
    print_status "Enabling and starting service..."
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable ${SERVICE_NAME}
    
    # Start service
    sudo systemctl start ${SERVICE_NAME}
    
    # Check service status
    if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
        print_success "Service started successfully"
        
        # Show service status
        print_status "Service status:"
        sudo systemctl status ${SERVICE_NAME} --no-pager -l
        
        # Show application URL
        print_success "Application is now running at: http://localhost:5000"
    else
        print_error "Service failed to start"
        print_status "Service logs:"
        sudo journalctl -u ${SERVICE_NAME} --no-pager -l
        exit 1
    fi
}

# Function to create management scripts
create_management_scripts() {
    print_status "Creating management scripts..."
    
    # Create start script
    cat > "$INSTALL_DIR/start_sniffer.sh" << 'EOF'
#!/bin/bash
echo "Starting WiFi Sniffer service..."
sudo systemctl start sniffer
sudo systemctl status sniffer --no-pager
EOF
    
    # Create stop script
    cat > "$INSTALL_DIR/stop_sniffer.sh" << 'EOF'
#!/bin/bash
echo "Stopping WiFi Sniffer service..."
sudo systemctl stop sniffer
echo "Service stopped"
EOF
    
    # Create restart script
    cat > "$INSTALL_DIR/restart_sniffer.sh" << 'EOF'
#!/bin/bash
echo "Restarting WiFi Sniffer service..."
sudo systemctl restart sniffer
sudo systemctl status sniffer --no-pager
EOF
    
    # Create status script
    cat > "$INSTALL_DIR/status_sniffer.sh" << 'EOF'
#!/bin/bash
echo "WiFi Sniffer Service Status:"
sudo systemctl status sniffer --no-pager
echo ""
echo "Recent logs:"
sudo journalctl -u sniffer --no-pager -n 20
EOF
    
    # Create logs script
    cat > "$INSTALL_DIR/logs_sniffer.sh" << 'EOF'
#!/bin/bash
echo "WiFi Sniffer Service Logs (last 50 lines):"
sudo journalctl -u sniffer --no-pager -n 50
EOF
    
    # Make scripts executable
    chmod +x "$INSTALL_DIR"/*_sniffer.sh
    
    print_success "Management scripts created in $INSTALL_DIR"
}

# Function to create uninstall script
create_uninstall_script() {
    print_status "Creating uninstall script..."
    
    cat > "$INSTALL_DIR/uninstall_sniffer.sh" << EOF
#!/bin/bash

echo "Uninstalling WiFi Sniffer..."

# Stop and disable service
sudo systemctl stop $SERVICE_NAME 2>/dev/null || true
sudo systemctl disable $SERVICE_NAME 2>/dev/null || true

# Remove service file
sudo rm -f /etc/systemd/system/${SERVICE_NAME}.service
sudo systemctl daemon-reload

# Remove udev rule
sudo rm -f /etc/udev/rules.d/99-usb-serial.rules
sudo udevadm control --reload-rules

# Remove management scripts
rm -f "$INSTALL_DIR"/*_sniffer.sh

echo "WiFi Sniffer uninstalled successfully"
echo "Note: Application files in $INSTALL_DIR are preserved"
EOF
    
    chmod +x "$INSTALL_DIR/uninstall_sniffer.sh"
    print_success "Uninstall script created"
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Check if service is running
    if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
        print_success "Service is running"
    else
        print_error "Service is not running"
        return 1
    fi
    
    # Check if application is accessible
    if command_exists curl; then
        if curl -s http://localhost:5000 > /dev/null; then
            print_success "Application is accessible at http://localhost:5000"
        else
            print_warning "Application may not be fully accessible yet"
        fi
    fi
    
    # Check Python environment
    if [ -f "$INSTALL_DIR/venv/bin/python" ]; then
        print_success "Python virtual environment is set up"
    else
        print_error "Python virtual environment not found"
        return 1
    fi
    
    print_success "Installation verification complete"
}

# Main installation function
main() {
    echo "=================================="
    echo "  WiFi Sniffer Installation"
    echo "=================================="
    echo ""
    
    # Check if running as root
    check_root
    
    # Check if we're in the sniffer directory
    if [ ! -f "app.py" ] || [ ! -f "sniffer.py" ]; then
        print_error "This script must be run from the sniffer application directory"
        print_status "Please navigate to the directory containing app.py and sniffer.py"
        exit 1
    fi
    
    print_status "Starting installation process..."
    echo ""
    
    # Run installation steps
    install_dependencies
    setup_directories
    setup_python_env
    setup_serial_permissions
    create_service
    start_service
    create_management_scripts
    create_uninstall_script
    
    echo ""
    print_success "Installation completed successfully!"
    echo ""
    print_status "Next steps:"
    print_status "1. Connect your serial device to $SERIAL_PORT"
    print_status "2. Access the application at: http://localhost:5000"
    print_status "3. Use the management scripts in $INSTALL_DIR for service control"
    echo ""
    print_status "Management commands:"
    print_status "  $INSTALL_DIR/status_sniffer.sh  - Check service status"
    print_status "  $INSTALL_DIR/logs_sniffer.sh    - View service logs"
    print_status "  $INSTALL_DIR/restart_sniffer.sh - Restart the service"
    print_status "  $INSTALL_DIR/uninstall_sniffer.sh - Uninstall everything"
    echo ""
    
    verify_installation
}

# Run main function
main "$@"