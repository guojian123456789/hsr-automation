@echo off
REM HSR Automation - Docker Build Script (Windows) - English Version
REM Usage: build_android_en.bat [debug|release|clean]

setlocal enabledelayedexpansion

echo ========================================
echo HSR Automation - Docker Build Tool
echo ========================================
echo.

REM Create log file
set LOG_FILE=build_log_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
set LOG_FILE=%LOG_FILE: =0%
echo Build log will be saved to: %LOG_FILE%
echo. > %LOG_FILE%

REM Check if Docker is installed
echo [CHECK] Checking if Docker is installed...
echo [CHECK] Checking if Docker is installed... >> %LOG_FILE%

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo [ERROR] Docker NOT detected!
    echo ========================================
    echo.
    echo Docker Desktop is not installed or not running.
    echo.
    echo Please follow these steps:
    echo.
    echo 1. Download Docker Desktop:
    echo    https://www.docker.com/products/docker-desktop
    echo.
    echo 2. Install Docker Desktop
    echo.
    echo 3. Start Docker Desktop (wait for the icon to turn green)
    echo.
    echo 4. Run this script again
    echo.
    echo ========================================
    echo [ERROR] Docker not installed >> %LOG_FILE%
    pause
    exit /b 1
)

docker --version
echo [SUCCESS] Docker is installed
echo [SUCCESS] Docker is installed >> %LOG_FILE%
echo.

REM Check if Docker is running
echo [CHECK] Checking if Docker is running...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo [ERROR] Docker is NOT running!
    echo ========================================
    echo.
    echo Docker Desktop is installed but not running.
    echo.
    echo Please:
    echo.
    echo 1. Start Docker Desktop
    echo.
    echo 2. Wait for Docker to fully start (icon turns green)
    echo.
    echo 3. Run this script again
    echo.
    echo ========================================
    echo [ERROR] Docker not running >> %LOG_FILE%
    pause
    exit /b 1
)

echo [SUCCESS] Docker is running
echo [SUCCESS] Docker is running >> %LOG_FILE%
echo.

REM Get current directory
set CURRENT_DIR=%CD%
echo [INFO] Current directory: %CURRENT_DIR%
echo [INFO] Current directory: %CURRENT_DIR% >> %LOG_FILE%

REM Get build type
set BUILD_TYPE=%1
if "%BUILD_TYPE%"=="" set BUILD_TYPE=debug
echo [INFO] Build type: %BUILD_TYPE%
echo [INFO] Build type: %BUILD_TYPE% >> %LOG_FILE%
echo.

REM Check if Dockerfile exists
if not exist "Dockerfile" (
    echo [INFO] Dockerfile does not exist, creating...
    echo [INFO] Creating Dockerfile... >> %LOG_FILE%
    (
        echo FROM ubuntu:22.04
        echo.
        echo ENV DEBIAN_FRONTEND=noninteractive
        echo.
        echo RUN apt-get update ^&^& apt-get install -y \
        echo     git zip unzip openjdk-17-jdk python3-pip \
        echo     autoconf libtool pkg-config zlib1g-dev \
        echo     libncurses5-dev libncursesw5-dev libtinfo5 \
        echo     cmake libffi-dev libssl-dev ^&^& \
        echo     rm -rf /var/lib/apt/lists/*
        echo.
        echo RUN pip3 install --upgrade pip ^&^& \
        echo     pip3 install buildozer cython==0.29.33
        echo.
        echo WORKDIR /app
        echo.
        echo CMD ["/bin/bash"]
    ) > Dockerfile
    echo [DONE] Dockerfile created
    echo [DONE] Dockerfile created >> %LOG_FILE%
    echo.
) else (
    echo [INFO] Dockerfile found
    echo [INFO] Dockerfile found >> %LOG_FILE%
    echo.
)

REM Build Docker image
echo ========================================
echo [STEP 1/3] Building Docker image
echo ========================================
echo.
echo This may take a few minutes, please wait...
echo.
echo [STEP 1/3] Building Docker image >> %LOG_FILE%

docker build -t hsr-android-builder . >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo [ERROR] Docker image build FAILED!
    echo ========================================
    echo.
    echo Please check the log file for detailed error:
    echo %LOG_FILE%
    echo.
    echo Common issues:
    echo 1. Network connection - Check your internet
    echo 2. Disk space - Ensure at least 5GB free space
    echo 3. Docker config - Try restarting Docker Desktop
    echo.
    echo ========================================
    pause
    exit /b 1
)

echo [SUCCESS] Docker image built successfully!
echo [SUCCESS] Docker image built successfully! >> %LOG_FILE%
echo.

REM Execute build based on type
if "%BUILD_TYPE%"=="clean" (
    echo ========================================
    echo [STEP 2/3] Cleaning build files
    echo ========================================
    echo.
    echo [STEP 2/3] Cleaning build files >> %LOG_FILE%
    
    docker run --rm -v "%CURRENT_DIR%:/app" hsr-android-builder bash -c "buildozer android clean && rm -rf .buildozer/ bin/" >> %LOG_FILE% 2>&1
    
    echo [DONE] Cleanup complete!
    echo [DONE] Cleanup complete! >> %LOG_FILE%
    echo.
    pause
    exit /b 0
)

REM Start building APK
echo ========================================
echo [STEP 2/3] Building APK (%BUILD_TYPE% version)
echo ========================================
echo.
echo IMPORTANT:
echo - First build will download Android SDK/NDK (about 1-2GB)
echo - Estimated time: 30 minutes to 1 hour
echo - Please ensure stable internet connection
echo - Do NOT close this window
echo.
echo Build started: %date% %time%
echo.
echo [STEP 2/3] Building APK >> %LOG_FILE%
echo Build started: %date% %time% >> %LOG_FILE%

if "%BUILD_TYPE%"=="release" (
    docker run --rm -v "%CURRENT_DIR%:/app" hsr-android-builder bash -c "cd /app && buildozer android release" 
) else (
    docker run --rm -v "%CURRENT_DIR%:/app" hsr-android-builder bash -c "cd /app && buildozer android debug"
)

set BUILD_ERROR=%errorlevel%

if %BUILD_ERROR% neq 0 (
    echo.
    echo ========================================
    echo [ERROR] Build FAILED!
    echo ========================================
    echo.
    echo Error code: %BUILD_ERROR%
    echo.
    echo Please check:
    echo 1. Error messages above
    echo 2. buildozer.spec configuration
    echo 3. Log file: %LOG_FILE%
    echo.
    echo For help, see:
    echo - BUILD_ANDROID_GUIDE.md
    echo - ANDROID_ADAPTATION_GUIDE.md
    echo.
    echo ========================================
    echo [ERROR] Build failed, error code: %BUILD_ERROR% >> %LOG_FILE%
    pause
    exit /b 1
)

REM Find generated APK
echo.
echo ========================================
echo [STEP 3/3] Looking for generated APK
echo ========================================
echo.

set APK_FOUND=0
if exist "bin" (
    for /r "bin" %%f in (*.apk) do (
        echo [APK FILE] %%f
        echo [APK SIZE] 
        dir "%%f" | find ".apk"
        echo.
        set APK_FOUND=1
        echo [APK FILE] %%f >> %LOG_FILE%
    )
)

if %APK_FOUND%==0 (
    echo [WARNING] APK file not found
    echo [WARNING] Please check bin directory
    echo.
    echo [WARNING] APK file not found >> %LOG_FILE%
)

echo.
echo ========================================
echo [SUCCESS] Build Complete!
echo ========================================
echo.
echo Build finished: %date% %time%
echo.
echo Next steps:
echo.
echo 1. Install to phone:
echo    adb install bin\hsrautomation-1.0-arm64-v8a-debug.apk
echo.
echo 2. View log:
echo    type %LOG_FILE%
echo.
echo ========================================
echo.
echo Build finished: %date% %time% >> %LOG_FILE%

pause




