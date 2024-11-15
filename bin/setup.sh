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

# Create the homelab-agent user if it doesn't exist
if id "homelab-agent" &>/dev/null; then
    info "User 'homelab-agent' already exists."
else
    info "Creating user 'homelab-agent'..."
    useradd -m -s /bin/bash homelab-agent
fi

# Switch to the homelab-agent user and set up the environment
info "Setting up the environment for 'homelab-agent'..."
sudo -u homelab-agent bash <<'EOF'
set -e
cd ~

# Create the "live" directory
echo "Creating 'live' directory..."
mkdir -p ~/live
cd ~/live

# Initialize git and set up the repository
echo "Initializing git repository..."
git init
git remote add origin https://github.com/briandeheus/homelab-agent.git

echo "Checking out 'main' branch..."
git fetch origin main
git checkout main

# Set up the virtual environment
echo "Creating virtual environment..."
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
cp /home/homelab-agent/live/.files/homelab-agent.service /etc/systemd/system/homelab-agent.service
systemctl daemon-reload
systemctl enable homelab-agent
systemctl start homelab-agent

# Final confirmation
info "Setup complete! Brian's Homelab Agent is running as a service. Run `systemctl status homelab-agent`"
