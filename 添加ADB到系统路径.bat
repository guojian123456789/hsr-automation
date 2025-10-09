@echo off
echo ========================================
echo ADB 路径配置工具
echo ========================================
echo.
echo 请输入你的 platform-tools 文件夹完整路径
echo 例如: C:\Users\你的用户名\Downloads\platform-tools
echo.
set /p ADB_PATH="ADB 路径: "
echo.
echo 正在添加到系统 PATH...
setx PATH "%PATH%;%ADB_PATH%"
echo.
echo ========================================
echo 配置完成！
echo 请关闭并重新打开命令提示符或PowerShell
echo 然后就可以在任何地方使用 adb 命令了
echo ========================================
pause


