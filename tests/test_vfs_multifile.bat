@echo off
echo ========================================
echo Testing VFS - Multiple Files
echo ========================================

cd /d "%~dp0.."

echo.
echo Test: Multiple files VFS
echo ----------------------------------------
python main.py --vfs tests\vfs_multifile.json --script tests\startup_basic.sh

pause