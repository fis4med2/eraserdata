# Metadata Protector

A cross-platform tool to automatically strip EXIF, GPS, and other metadata from photos and screenshots. Protects your privacy by removing sensitive location data before sharing images online.

[![Windows](https://img.shields.io/badge/Windows-%230078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white)](https://archlinux.org)
[![Fedora](https://img.shields.io/badge/Fedora-FF5A36?style=for-the-badge&logo=fedora&logoColor=white)](https://fedoraproject.org)
[![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)](https://debian.org)
[![openSUSE](https://img.shields.io/badge/openSUSE-1F549B?style=for-the-badge&logo=opensuse&logoColor=white)](https://opensuse.org)
[![Red Hat](https://img.shields.io/badge/Red_Hat-FC6E41?style=for-the-badge&logo=red-hat&logoColor=white)](https://redhat.com)
[![Manjaro](https://img.shields.io/badge/Manjaro-35BF7C?style=for-the-badge&logo=manjaro&logoColor=white)](https://manjaro.org)
[![CentOS](https://img.shields.io/badge/CentOS-FF5252?style=for-the-badge&logo=centos&logoColor=white)](https://centos.org)
[![FreeBSD](https://img.shields.io/badge/FreeBSD-4A9FD1?style=for-the-badge&logo=freebsd&logoColor=white)](https://freebsd.org)

## Features

- **Background Watching** – Automatically monitors folders and cleans new images as they appear
- **One-Time Cleaning** – Process a specific folder and remove metadata from all images
- **Auto-Updates** – Downloads the latest version from GitHub releases
- **Cross-Platform** – Works on Windows, macOS, and Linux
- **Configurable** – Customize which folders to monitor and auto-update settings

## Quick Start

### Windows

1. **Build the installer**:
   ```bash
   ./build_windows.bat
   ```

2. **Run the installer** – Double-click `MetadataProtector.exe` or run it from the command line.

3. **Or use the launcher** – After installation, run:
   ```bash
   python launcher.py
   ```

### Linux

1. **Build the distribution**:
   ```bash
   ./build_linux.sh
   ```

2. **Extract and run**:
   ```bash
   tar -xzf MetadataProtector.tar.gz
   cd MetadataProtector
   python launcher.py
   ```

   Or make it executable and run directly:
   ```bash
   chmod +x launcher.py
   ./launcher.py
   ```

### Universal Linux (works on any distro)

The tar.gz package is distro-agnostic. It works on Ubuntu, Arch, Fedora, Debian, openSUSE, Manjaro, CentOS, Red Hat, and all other Linux distributions without modification.

Just extract and run with Python 3.8+:

```bash
tar -xzf MetadataProtector.tar.gz
cd MetadataProtector
pip install -r requirements.txt
python launcher.py
```

## Project Structure

```
eraserdata--main/
├── watch_metadata.py      # Background watcher (metadata cleaner)
├── clean_metadata.py       # One-time cleanup tool
├── launcher.py             # CLI launcher with config & updater
├── requirements.txt        # Python dependencies
├── build_linux.sh          # Build script for Linux tar.gz
├── build_windows.bat       # Build script for Windows .exe
└── README.md              # This file
```

## Configuration

The launcher maintains a configuration file (`~/.metadata_config.json`) that stores:

- List of folders to monitor
- Whether to auto-update from GitHub
- Version tracking

You can edit this file manually or use the menu in `launcher.py` to manage folders.

## Updating

The launcher automatically checks for newer versions from GitHub releases and offers to update. Simply run:

```bash
python launcher.py
```

## Requirements

- **Python 3.8+** (both Windows and Linux)
- **Pillow** and **watchdog** (installed via `requirements.txt`)

## License

MIT – see [LICENSE](LICENSE) for details.

## Support

- **Windows**: Right-click the `.exe` → Properties → Run as administrator
- **Linux**: Extract the tarball and run `./launcher.py`
- **Updates**: The launcher handles automatic updates from GitHub releases

## Troubleshooting

- **Can't find a folder**: Ensure the path exists and is accessible
- **Update fails**: Check internet connection and GitHub API rate limits
- **Clean mode fails**: Some files may be locked by other processes

## Contributing

Feel free to submit issues or pull requests. Improvements are welcome!