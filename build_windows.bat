@echo off
REM Build script for Windows distribution
REM Creates a standalone .exe using PyInstaller
REM
REM Usage: build_windows.bat

setlocal

set "PROJECT_DIR=%CD%"
set "APP_NAME=MetadataProtector"
set "BUILD_DIR=%PROJECT_DIR%\build\windows"

echo Building Windows distribution...
echo Project: %PROJECT_DIR%

REM Clean previous build
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"

REM Install PyInstaller if not present
python -m pip install pyinstaller >nul 2>&1

REM Build the executable
cd "%PROJECT_DIR%"
pyinstaller --onefile --windowed --name "%APP_NAME%" --noconfirm launcher.py

REM Move the built executable to build directory
if exist "dist\%APP_NAME%.exe" (
    copy "dist\%APP_NAME%.exe" "%BUILD_DIR%\%APP_NAME%.exe"
    echo.
    echo Done! Created: %BUILD_DIR%\%APP_NAME%.exe
    echo.
    echo To install on Windows:
    echo   1. Run %APP_NAME%.exe as administrator
    echo   2. Or copy to a folder and run from there
) else (
    echo ERROR: Build failed. Check the console output above.
    exit /b 1
)