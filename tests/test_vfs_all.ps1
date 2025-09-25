# PowerShell test script for VFS functionality

# Change to parent directory where main.py is located
Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "========================================" -ForegroundColor Green
Write-Host "VFS Testing Suite" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green

$tests = @(
    @{
        Name = "Minimal VFS"
        VFS = "tests\vfs_minimal.json"
        Script = "tests\startup_basic.sh"
        Description = "Simple VFS with one file"
    },
    @{
        Name = "Multi-file VFS"
        VFS = "tests\vfs_multifile.json" 
        Script = "tests\startup_basic.sh"
        Description = "VFS with multiple files"
    },
    @{
        Name = "Complex VFS Structure"
        VFS = "tests\vfs_complex.json"
        Script = "tests\startup_full_test.sh"
        Description = "Complex VFS with 3+ directory levels"
    }
)

foreach ($test in $tests) {
    Write-Host "`n$('-' * 50)" -ForegroundColor Blue
    Write-Host "Test: $($test.Name)" -ForegroundColor Yellow
    Write-Host "Description: $($test.Description)" -ForegroundColor Gray
    Write-Host "Command: python main.py --vfs $($test.VFS) --script $($test.Script)" -ForegroundColor Cyan
    Write-Host "$('-' * 50)" -ForegroundColor Blue
    
    python main.py --vfs $test.VFS --script $test.Script
    
    Write-Host "`nPress Enter to continue to next test..." -ForegroundColor Green
    Read-Host
}

Write-Host "`nAll VFS tests completed!" -ForegroundColor Green
Read-Host "Press Enter to exit"