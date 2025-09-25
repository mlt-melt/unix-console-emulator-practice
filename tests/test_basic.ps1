# Простой тест для UNIX Console Emulator

# Переходим в родительскую директорию  
Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "========================================" -ForegroundColor Green
Write-Host "UNIX Console Emulator Test" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nTest 1: Startup script" -ForegroundColor Yellow
python main.py --script "tests\startup_basic.sh"

Write-Host "`nTest 2: VFS + script" -ForegroundColor Yellow  
python main.py --vfs "./my_vfs" --script "tests\startup_basic.sh"

Write-Host "`nAll tests completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"