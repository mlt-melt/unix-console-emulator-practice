# Тесты для UNIX Console Emulator

## Структура
- Скрипты запуска: `startup_basic.sh`, `startup_full_test.sh`
- VFS-файлы: `vfs_minimal.json`, `vfs_multifile.json`, `vfs_complex.json`
- Тесты Windows: `test_basic.bat`, `test_vfs_minimal.bat`, `test_vfs_multifile.bat`, `test_vfs_complex.bat`
- Тесты PowerShell: `test_basic.ps1`, `test_vfs_all.ps1`

## Запуск
Базовые тесты:
```cmd
test_basic.bat
.\test_basic.ps1
```
VFS-тесты:
```cmd
test_vfs_minimal.bat
test_vfs_multifile.bat
test_vfs_complex.bat
.\test_vfs_all.ps1
```
Ручное тестирование:
```bash
python main.py --vfs tests\vfs_minimal.json --script tests\startup_basic.sh
python main.py --vfs tests\vfs_complex.json --script tests\startup_full_test.sh
python main.py --vfs tests\vfs_complex.json --interactive
```
│       │   ├── main.py
│       │   └── data.json
│       └── personal/
│           ├── diary.txt
│           └── photos/vacation.jpg
├── usr/
│   ├── bin/ (python, bash)
│   └── lib/ (libtest.so)
└── etc/
    ├── hosts
    └── config/app.conf
```