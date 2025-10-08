#!/bin/bash

# HSR Automation - Android构建脚本
# 使用方法：bash build_android.sh [debug|release|clean]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}HSR Automation - Android构建工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查是否在Linux/macOS环境
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo -e "${RED}错误：Buildozer只能在Linux或macOS上运行${NC}"
    echo -e "${YELLOW}请使用WSL2、虚拟机或Docker来构建${NC}"
    exit 1
fi

# 检查buildozer是否安装
if ! command -v buildozer &> /dev/null; then
    echo -e "${YELLOW}警告：未检测到buildozer${NC}"
    echo -e "${YELLOW}正在安装buildozer...${NC}"
    pip3 install --upgrade buildozer cython==0.29.33
fi

# 检查Java是否安装
if ! command -v java &> /dev/null; then
    echo -e "${RED}错误：未检测到Java${NC}"
    echo -e "${YELLOW}请先安装Java 17：sudo apt install openjdk-17-jdk${NC}"
    exit 1
fi

# 获取构建类型
BUILD_TYPE=${1:-debug}

case $BUILD_TYPE in
    debug)
        echo -e "${GREEN}开始构建Debug版本...${NC}"
        buildozer android debug
        ;;
    release)
        echo -e "${GREEN}开始构建Release版本...${NC}"
        buildozer android release
        ;;
    clean)
        echo -e "${YELLOW}清理构建文件...${NC}"
        buildozer android clean
        rm -rf .buildozer/
        rm -rf bin/
        echo -e "${GREEN}清理完成！${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}未知的构建类型：$BUILD_TYPE${NC}"
        echo -e "${YELLOW}使用方法：bash build_android.sh [debug|release|clean]${NC}"
        exit 1
        ;;
esac

# 检查构建是否成功
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}构建成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    # 查找生成的APK
    APK_FILE=$(find bin/ -name "*.apk" -type f 2>/dev/null | head -n 1)
    
    if [ -n "$APK_FILE" ]; then
        echo -e "${GREEN}APK文件位置：${NC}$APK_FILE"
        echo -e "${GREEN}文件大小：${NC}$(du -h "$APK_FILE" | cut -f1)"
        echo ""
        echo -e "${YELLOW}安装到手机：${NC}adb install $APK_FILE"
    fi
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}构建失败！${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}请查看日志文件获取详细信息${NC}"
    exit 1
fi




