@echo off
REM HSR Automation - Local Build (No Docker)
REM Direct Python build using Buildozer

setlocal enabledelayedexpansion

echo ========================================
echo HSR Automation - Local Build Tool
echo ========================================
echo.

REM Check if Python is installed
echo [CHECK] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version
echo [SUCCESS] Python is installed
echo.

REM Check if pip is available
echo [CHECK] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found!
    pause
    exit /b 1
)

echo [SUCCESS] pip is available
echo.

REM Check if buildozer is installed
echo [CHECK] Checking Buildozer...
pip show buildozer >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Buildozer not installed, installing...
    echo.
    pip install buildozer cython==0.29.33
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Buildozer
        pause
        exit /b 1
    )
)

echo [SUCCESS] Buildozer is ready
echo.

REM Note about WSL requirement
echo ========================================
echo IMPORTANT INFORMATION
echo ========================================
echo.
echo Buildozer requires Linux/WSL to build Android APKs.
echo Docker was the recommended approach, but due to network
echo issues, here are alternative solutions:
echo.
echo OPTION A: Use GitHub Actions (Recommended)
echo   - Build in the cloud, no local setup needed
echo   - See: build_on_github.md
echo.
echo OPTION B: Use WSL (Windows Subsystem for Linux)
echo   - Install WSL: wsl --install
echo   - Run buildozer inside WSL
echo   - See: build_with_wsl.md
echo.
echo OPTION C: Use a cloud VM
echo   - Use free services like Google Colab
echo   - See: build_on_cloud.md
echo.
echo ========================================
echo.

pause

