#!/usr/bin/env python3
"""
Metadata Protector Launcher - Cross-platform config manager and updater.

Features:
- Configuration UI for watched folders
- Automatic updates from GitHub releases
- Background metadata scrubbing

Usage:
    python launcher.py

On Windows, can be compiled to .exe with PyInstaller for standalone use.
"""

import sys
import os
import json
import platform
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / ".metadata_config.json"
GITHUB_REPO = "eraserdata/eraserdata--main"


def get_path_for_platform(path: str) -> Path:
    if sys.platform == "win32":
        return Path(path.replace("/", "\\"))
    return Path(path)


def load_config() -> dict:
    default_config = {
        "watched_folders": [str(Path.home() / "Pictures")],
        "auto_update": True,
        "check_on_start": True,
        "version": "1.0.0",
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**default_config, **json.load(f)}
        except (json.JSONDecodeError, IOError):
            pass
    return default_config


def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_latest_version() -> str:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MetadataProtector"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("tag_name", "1.0.0").lstrip("v")
    except Exception:
        return None


def download_latest_release() -> Path:
    version = get_latest_version()
    if not version:
        return None

    url = f"https://github.com/{GITHUB_REPO}/releases/download/v{version}/eraserdata.zip"

    cache_dir = Path.home() / ".metadata_cache"
    cache_dir.mkdir(exist_ok=True)
    zip_path = cache_dir / "eraserdata.zip"

    try:
        urllib.request.urlretrieve(url, zip_path)
        return zip_path
    except Exception as e:
        print(f"Download failed: {e}")
        return None


def extract_and_update(zip_path: Path) -> bool:
    if not zip_path or not zip_path.exists():
        return False

    extract_dir = Path.home() / ".metadata_update"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir()

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_dir)

        app_dir = extract_dir / "eraserdata"
        target_dir = Path(__file__).parent

        for item in ["watch_metadata.py", "clean_metadata.py", "launcher.py", "requirements.txt"]:
            src = app_dir / item
            if src.exists():
                shutil.copy2(src, target_dir / item)

        return True
    except Exception as e:
        print(f"Update failed: {e}")
        return False


def check_for_updates() -> bool:
    config = load_config()
    if not config.get("auto_update", True):
        return False

    latest = get_latest_version()
    if not latest:
        return False

    current = config.get("version", "1.0.0")
    if latest != current:
        print(f"New version {latest} available (current: {current})")
        return True
    return False


def perform_update():
    print("Checking for updates...")
    zip_path = download_latest_release()
    if zip_path:
        print("Downloading update...")
        if extract_and_update(zip_path):
            print("Update complete! Please restart the application.")
            if zip_path.exists():
                zip_path.unlink()
            cache_dir = Path.home() / ".metadata_cache"
            if cache_dir.exists():
                shutil.rmtree(cache_dir)
            return True
    return False


def show_config_menu():
    config = load_config()
    print("\n📁 Watched Folders Configuration")
    print("-" * 40)

    for i, folder in enumerate(config.get("watched_folders", []), 1):
        path = get_path_for_platform(folder)
        exists = "✓" if path.exists() else "✗"
        print(f"{i}. [{exists}] {folder}")

    print("\nOptions:")
    print("A. Add folder")
    print("R. Remove folder")
    print("C. Clear all folders")
    print("S. Save and exit")

    choice = input("\nChoose: ").strip().lower()

    if choice == "a":
        path = input("Enter folder path: ").strip()
        if path:
            config.setdefault("watched_folders", []).append(path)
    elif choice == "r":
        try:
            idx = int(input("Enter number to remove: ")) - 1
            if 0 <= idx < len(config.get("watched_folders", [])):
                config["watched_folders"].pop(idx)
        except ValueError:
            pass
    elif choice == "c":
        config["watched_folders"] = []
    elif choice == "s":
        pass

    save_config(config)
    print("Configuration saved.")


def write_watch_script():
    config = load_config()
    folders = config.get("watched_folders", [])

    script_path = Path(__file__).parent / "watch_metadata.py"

    if script_path.exists():
        with open(script_path, "r") as f:
            content = f.read()

        start_marker = "# ======= CONFIG:"
        end_marker = "# ==============="
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker, start_idx)

        if start_idx != -1 and end_idx != -1:
            folders_code = "WATCHED_FOLDERS = [\n"
            for folder in folders:
                if sys.platform == "win32":
                    folders_code += f'    r"{folder}",\n'
                else:
                    folders_code += f'    os.path.expanduser("{folder}"),\n'
            folders_code += "]\n"

            new_content = content[:start_idx] + folders_code + content[end_idx + len(end_marker):]

            with open(script_path, "w") as f:
                f.write(new_content)


def run_clean_mode():
    folder = input("Enter folder to clean: ").strip()
    if not folder:
        print("No folder specified.")
        return

    overwrite = input("Overwrite originals? (y/N): ").strip().lower() == "y"

    cmd = [sys.executable, "clean_metadata.py", folder]
    if overwrite:
        cmd.append("--overwrite")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Cleaning failed: {e}")


def run_watch_mode():
    write_watch_script()
    print("Starting metadata watcher...")
    try:
        subprocess.run([sys.executable, "watch_metadata.py"], check=True)
    except KeyboardInterrupt:
        print("\nWatcher stopped.")


def main():
    print("=" * 50)
    print("  Metadata Protector Launcher")
    print("=" * 50)

    if config.get("check_on_start", True) and check_for_updates():
        if input("Update now? (y/N): ").strip().lower() == "y":
            perform_update()
            return

    print("\nMenu:")
    print("1. Configure folders")
    print("2. Clean existing folder")
    print("3. Start watcher (background)")
    print("4. Exit")

    choice = input("\nSelect: ").strip()

    if choice == "1":
        show_config_menu()
    elif choice == "2":
        run_clean_mode()
    elif choice == "3":
        run_watch_mode()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    config = load_config()
    main()