# Quick Setup Guide

## For Non-Nix Users (Windows, macOS, or Linux without Nix)

### Prerequisites
- Python 3.8 or higher installed
- A working camera (built-in or USB)

### Step 1: Install Dependencies

**Option A: Using pip (system-wide)**
```bash
pip install -r requirements.txt
```

**Option B: Using virtual environment (recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Server

```bash
python src/main.py
```

The server will start on `http://0.0.0.0:5000`

### Step 3: Access the Camera Feed

1. **From the same computer:** Open `http://localhost:5000` in your browser
2. **From other devices:** 
   - Find your IP: `ip addr show` (Linux) or `ipconfig` (Windows)
   - Open `http://<YOUR_IP>:5000` in a browser

### Troubleshooting Common Issues

**Issue: "No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**Issue: "Camera not available"**
- Try different camera index: `set CAMERA_INDEX=1` (Windows) or `export CAMERA_INDEX=1` (Linux/macOS)
- Make sure camera isn't used by another application

**Issue: "Permission denied" (Linux)**
```bash
# Add your user to video group
sudo usermod -a -G video $USER
# Log out and log back in for changes to take effect
```

**Issue: "Cannot access from other devices"**
- Disable firewall temporarily to test
- Ensure both devices are on the same WiFi network

## For NixOS Users

```bash
# Enter development environment
nix develop

# Run the server
python src/main.py
```

That's it! All dependencies are provided by the Nix flake.
