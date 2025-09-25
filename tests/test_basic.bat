@echo off
echo ========================================
echo UNIX Console Emulator Test
echo ========================================

cd /d "%~dp0.."

echo.
echo Test 1: Startup script
echo ----------------------------------------
python main.py --script tests\startup_basic.sh

echo.
echo Test 2: Demo mode
echo ----------------------------------------  
python main.py --demo

echo.
echo Test 3: Help
echo ----------------------------------------
python main.py --help

pause