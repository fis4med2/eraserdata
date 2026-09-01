#!/bin/bash
# Build script for Linux distribution
# Creates a tar.gz archive with all necessary files
#
# Usage: ./build_linux.sh

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$OUTPUT_DIR/build"
ARCHIVE_NAME="MetadataProtector"
ARCHIVE_PATH="$OUTPUT_DIR/$ARCHIVE_NAME.tar.gz"

echo "Building Linux distribution..."
echo "Project: $PROJECT_DIR"
echo "Output:  $ARCHIVE_PATH"

# Clean previous build
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Create build directory and copy files there
mkdir -p "$BUILD_DIR"
cp "$PROJECT_DIR/watch_metadata.py" "$BUILD_DIR/"
cp "$PROJECT_DIR/clean_metadata.py" "$BUILD_DIR/"
cp "$PROJECT_DIR/launcher.py" "$BUILD_DIR/"
cp "$PROJECT_DIR/requirements.txt" "$BUILD_DIR/"

# Create the tar.gz archive
cd "$OUTPUT_DIR"
tar -czf "$ARCHIVE_PATH" -C "$BUILD_DIR" .

# Clean up build directory
rm -rf "$BUILD_DIR"

echo ""
echo "Done! Created: $ARCHIVE_PATH"
echo ""
echo "To install on Linux:"
echo "  tar -xzf $ARCHIVE_PATH -C /tmp/"
echo "  chmod +x /tmp/MetadataProtector/launcher.py"
echo "  /tmp/MetadataProtector/launcher.py"