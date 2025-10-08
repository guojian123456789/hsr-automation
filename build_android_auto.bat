@echo off
REM HSR Automation - Docker Build Script (Automated, No Pause)
REM Usage: build_android_auto.bat [debug|release|clean]

setlocal enabledelayedexpansion

echo ========================================
echo HSR Automation - Docker Build Tool
echo ========================================
echo.

REM Create log file
set LOG_FILE=build_log_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
set LOG_FILE=%LOG_FILE: =0%
echo Build log: %LOG_FILE%
echo. > %LOG_FILE%

REM Check if Docker is installed
echo [CHECK] Checking if Docker is installed...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker NOT detected!
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo [ERROR] Docker not installed >> %LOG_FILE%
    exit /b 1
)

docker --version
echo [SUCCESS] Docker is installed
echo.

REM Check if Docker is running
echo [CHECK] Checking if Docker is running...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is NOT running!
    echo Please start Docker Desktop and try again.
    echo [ERROR] Docker not running >> %LOG_FILE%
    exit /b 1
)

echo [SUCCESS] Docker is running
echo.

REM Get current directory
set CURRENT_DIR=%CD%
echo [INFO] Current directory: %CURRENT_DIR%

REM Get build type
set BUILD_TYPE=%1
if "%BUILD_TYPE%"=="" set BUILD_TYPE=debug
echo [INFO] Build type: %BUILD_TYPE%
echo.

REM Check if Dockerfile exists
if not exist "Dockerfile" (
    echo [INFO] Creating Dockerfile...
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
    echo.
) else (
    echo [INFO] Dockerfile found
    echo.
)

REM Build Docker image
echo ========================================
echo [STEP 1/3] Building Docker image
echo ========================================
echo.
echo This may take a few minutes...
echo.

docker build -t hsr-android-builder . >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker image build FAILED!
    echo See log file: %LOG_FILE%
    exit /b 1
)

echo [SUCCESS] Docker image built!
echo.

REM Execute build based on type
if "%BUILD_TYPE%"=="clean" (
    echo ========================================
    echo [STEP 2/3] Cleaning build files
    echo ========================================
    echo.
    
    docker run --rm -v "%CURRENT_DIR%:/app" hsr-android-builder bash -c "buildozer android clean && rm -rf .buildozer/ bin/" >> %LOG_FILE% 2>&1
    
    echo [DONE] Cleanup complete!
    echo.
    exit /b 0
)

REM Start building APK
echo ========================================
echo [STEP 2/3] Building APK (%BUILD_TYPE%)
echo ========================================
echo.
echo IMPORTANT:
echo - First build downloads Android SDK/NDK (~1-2GB)
echo - Estimated time: 30-60 minutes
echo - Please wait, do NOT close this window
echo.
echo Build started: %date% %time%
echo.

if "%BUILD_TYPE%"=="release" (
    docker run --rm -v "%CURRENT_DIR%:/app" hsr-android-builder bash -c "cd /app && buildozer android release" 
) else (
    docker run --rm -v "%CURRENT_DIR%:/app" hsr-android-builder bash -c "cd /app && buildozer android debug"
)

set BUILD_ERROR=%errorlevel%

if %BUILD_ERROR% neq 0 (
    echo.
    echo [ERROR] Build FAILED! Error code: %BUILD_ERROR%
    echo Please check log file: %LOG_FILE%
    echo.
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
        dir "%%f" | find ".apk"
        echo.
        set APK_FOUND=1
    )
)

if %APK_FOUND%==0 (
    echo [WARNING] APK file not found
    echo Please check bin directory
    echo.
)

echo.
echo ========================================
echo [SUCCESS] Build Complete!
echo ========================================
echo.
echo Build finished: %date% %time%
echo.
echo Next steps:
echo 1. Install: adb install bin\hsrautomation-1.0-arm64-v8a-debug.apk
echo 2. View log: type %LOG_FILE%
echo.
echo ========================================
echo.

exit /b 0

