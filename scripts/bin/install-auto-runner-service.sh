#!/bin/bash

# Auto Tool Runner Service Installer
# =================================

set -e

echo "🔧 Installing Auto Tool Runner as systemd service..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run as root (use sudo)"
    exit 1
fi

# Get the current user
CURRENT_USER=$(logname || echo $SUDO_USER)
if [ -z "$CURRENT_USER" ]; then
    echo "❌ Could not determine current user"
    exit 1
fi

echo "👤 Installing for user: $CURRENT_USER"

# Get the project directory
PROJECT_DIR="/home/$CURRENT_USER/shadow-link-industries/DEMO-LinkOps"

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found: $PROJECT_DIR"
    exit 1
fi

# Update the service file with the correct user and paths
sed -i "s/User=jimjrxieb/User=$CURRENT_USER/g" "$PROJECT_DIR/scripts/auto-runner.service"
sed -i "s/Group=jimjrxieb/Group=$CURRENT_USER/g" "$PROJECT_DIR/scripts/auto-runner.service"
sed -i "s|WorkingDirectory=/home/jimjrxieb/shadow-link-industries/DEMO-LinkOps|WorkingDirectory=$PROJECT_DIR|g" "$PROJECT_DIR/scripts/auto-runner.service"
sed -i "s|ExecStart=/usr/bin/python3 /home/jimjrxieb/shadow-link-industries/DEMO-LinkOps/scripts/auto_runner.py|ExecStart=/usr/bin/python3 $PROJECT_DIR/scripts/auto_runner.py|g" "$PROJECT_DIR/scripts/auto-runner.service"
sed -i "s|Environment=PYTHONPATH=/home/jimjrxieb/shadow-link-industries/DEMO-LinkOps|Environment=PYTHONPATH=$PROJECT_DIR|g" "$PROJECT_DIR/scripts/auto-runner.service"
sed -i "s|ReadWritePaths=/home/jimjrxieb/shadow-link-industries/DEMO-LinkOps|ReadWritePaths=$PROJECT_DIR|g" "$PROJECT_DIR/scripts/auto-runner.service"

# Copy service file to systemd directory
cp "$PROJECT_DIR/scripts/auto-runner.service" /etc/systemd/system/linkops-auto-runner.service

# Reload systemd
systemctl daemon-reload

# Enable the service
systemctl enable linkops-auto-runner.service

echo "✅ Service installed successfully!"
echo ""
echo "📋 Service Information:"
echo "  - Service name: linkops-auto-runner"
echo "  - Status: $(systemctl is-enabled linkops-auto-runner.service)"
echo "  - Working directory: $PROJECT_DIR"
echo ""
echo "🚀 To start the service:"
echo "  sudo systemctl start linkops-auto-runner"
echo ""
echo "📊 To check status:"
echo "  sudo systemctl status linkops-auto-runner"
echo ""
echo "📝 To view logs:"
echo "  sudo journalctl -u linkops-auto-runner -f"
echo ""
echo "🛑 To stop the service:"
echo "  sudo systemctl stop linkops-auto-runner" 