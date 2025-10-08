@echo off
REM Docker Environment Check Tool

echo ========================================
echo Docker Environment Check
echo ========================================
echo.

echo [1/4] Checking if Docker is installed...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Docker is NOT installed!
    echo.
    echo Please download and install Docker Desktop:
    echo https://www.docker.com/products/docker-desktop
    echo.
    goto :end
) else (
    docker --version
    echo [OK] Docker is installed
    echo.
)

echo [2/4] Checking if Docker is running...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Docker is NOT running!
    echo.
    echo Please start Docker Desktop and run this script again.
    echo.
    goto :end
) else (
    echo [OK] Docker is running
    echo.
)

echo [3/4] Checking Docker images...
docker images | find "hsr-android-builder" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Build image not found (normal for first run)
    echo.
) else (
    echo [OK] Build image found
    docker images | find "hsr-android-builder"
    echo.
)

echo [4/4] Checking required files...
if exist "Dockerfile" (
    echo [OK] Dockerfile exists
) else (
    echo [!] Dockerfile not found (will be auto-created)
)

if exist "buildozer.spec" (
    echo [OK] buildozer.spec exists
) else (
    echo [X] buildozer.spec NOT found!
    echo     This is a required file. Please check your project directory.
)

if exist "main.py" (
    echo [OK] main.py exists
) else (
    echo [X] main.py NOT found!
    echo     Please make sure you are in the correct project directory.
)

echo.
echo ========================================
echo Environment Check Complete!
echo ========================================
echo.

REM Check if all conditions are met
docker --version >nul 2>&1
if %errorlevel% neq 0 goto :end

docker ps >nul 2>&1
if %errorlevel% neq 0 goto :end

if not exist "buildozer.spec" goto :end
if not exist "main.py" goto :end

echo [OK] All checks passed! Ready to build.
echo.
echo Run this command to start building:
echo     build_android_docker_fixed.bat
echo.
goto :end

:end
echo ========================================
pause




