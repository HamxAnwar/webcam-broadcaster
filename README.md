# Camera Server

A Python-based camera streaming server that runs on your PC/laptop and makes your camera accessible on your local network.

## Features

- Live video streaming via MJPEG
- Capture snapshots
- View camera status (resolution, FPS, camera index)
- Beautiful web interface
- Runs on local network IP
- Full camera permissions

## Requirements

- Python 3.8 or higher
- A compatible camera (USB or built-in)
- For NixOS users: `nix develop` support
- For other systems: pip

## Installation & Setup

### Option 1: Using Nix (Recommended for NixOS)

1. Enter the development environment:
   ```bash
   nix develop
   ```

The Python packages are already provided by the Nix flake.

### Option 2: Using pip (For non-Nix systems)

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

### Nix users:
```bash
nix develop
python src/main.py
```

### Non-Nix users:
```bash
# Activate virtual environment first (if using one)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
python src/main.py
```

The server will start on `http://0.0.0.0:5000`

## Accessing from Other Devices

Find your IP address:

**Linux/macOS:**
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```bash
ipconfig
```

Then access from any device on the same network:
```
http://<YOUR_IP_ADDRESS>:5000
```

## Configuration

Environment variables:

- `CAMERA_INDEX`: Camera device index (default: 0) - try 0, 1, 2, etc.
- `HOST`: Host to bind to (default: 0.0.0.0)
- `PORT`: Port to listen on (default: 5000)

**Linux/macOS:**
```bash
export CAMERA_INDEX=1
export PORT=8080
python src/main.py
```

**Windows (PowerShell):**
```powershell
$env:CAMERA_INDEX=1
$env:PORT=8080
python src/main.py
```

**Windows (CMD):**
```cmd
set CAMERA_INDEX=1
set PORT=8080
python src/main.py
```

## Project Structure

```
camera-server/
├── flake.nix           # Nix flake for NixOS users
├── requirements.txt     # Python dependencies for pip users
├── README.md           # This file
├── .gitignore         # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── camera.py       # Camera handling module
│   └── main.py        # Flask application
├── static/            # Static assets (empty for now)
└── templates/
    └── index.html     # Web interface
```

## API Endpoints

- `GET /` - Web interface
- `GET /video_feed` - Live video stream (MJPEG)
- `GET /api/status` - Camera status information (JSON)
- `GET /api/snapshot` - Capture a snapshot (returns JPEG image)

## Testing Your Camera

Before running the server, verify your camera is accessible:

**Linux:**
```bash
ls -l /dev/video*
v4l2-ctl --list-devices  # if v4l-utils is installed
```

**Windows:**
Check if your camera appears in Device Manager under "Imaging devices" or "Cameras"

**macOS:**
```bash
system_profiler SPCameraDataType
```

## Troubleshooting

### Camera not accessible

**Linux:**
- Check camera permissions: Ensure your user has access to `/dev/video*`
- Verify camera index: Try different `CAMERA_INDEX` values (0, 1, 2, etc.)
- Check camera device: `ls -l /dev/video*`

**Windows:**
- Ensure no other application is using the camera
- Check Windows privacy settings: Settings → Privacy → Camera
- Try different camera index values

**macOS:**
- Check System Preferences → Security & Privacy → Privacy → Camera
- Ensure your terminal has camera access permissions

### Cannot access from other devices

- Check firewall settings
- Ensure server is binding to `0.0.0.0`
- Verify both devices are on the same network
- Try disabling VPN or proxy

### Video not showing

- Check if another application is using the camera
- Verify camera is working with system camera app
- Try a different `CAMERA_INDEX` value
- Check system logs for errors

### Import errors (pip users)

If you get import errors, try reinstalling dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Camera shows black screen

- Check if camera has a physical privacy cover
- Ensure proper lighting
- Try different camera resolution settings in `src/camera.py`

## Dependencies

### Python Packages (see `requirements.txt`):
- `flask==3.0.0` - Web framework
- `opencv-python==4.8.1.78` - Camera capture
- `jinja2==3.1.2` - Template engine (Flask dependency)
- `werkzeug==3.0.1` - WSGI utilities (Flask dependency)
- `pillow==10.1.0` - Image processing

### Nix Packages (see `flake.nix`):
- `python312` - Python interpreter
- `python312Packages.*` - Python packages
- `v4l-utils` - Video4Linux utilities (camera testing)
- `ffmpeg` - Video processing utilities

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
