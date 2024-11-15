#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print info messages
info() {
    echo -e "\033[1;32m[INFO]\033[0m $1"
}

# Function to print error messages
error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# Switch to the homelab-agent user and set up the environment
info "Update Homelab Agent"
sudo -u homelab-agent bash <<'EOF'
set -e
cd ~/live

echo "Checking out 'main' branch..."
git fetch origin main
git checkout main

python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt not found in repository."
fi
EOF

# Switch back to the root user
info "Switching back to root user."

# Set up and enable the systemd service
info "Setting up and enabling systemd service..."
systemctl restart homelab-agent

# Final confirmation
info "Update complete! Homelab-agent restarted."
