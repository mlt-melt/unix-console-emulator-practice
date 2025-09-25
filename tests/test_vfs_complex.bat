@echo off
echo ========================================
echo Testing VFS - Complex Structure
echo ========================================

cd /d "%~dp0.."

echo.
echo Test: Complex VFS with 3+ directory levels
echo ----------------------------------------
python main.py --vfs tests\vfs_complex.json --script tests\startup_full_test.sh

pause