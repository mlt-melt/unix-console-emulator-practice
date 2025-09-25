@echo off
echo ========================================
echo Testing VFS - Minimal
echo ========================================

cd /d "%~dp0.."

echo.
echo Test: Minimal VFS (1 file)
echo ----------------------------------------
python main.py --vfs tests\vfs_minimal.json --script tests\startup_basic.sh

pause