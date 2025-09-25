# UNIX Console Emulator - Этапы 1-3

## Описание

UNIX Console Emulator - проект эмуляции консоли UNIX с поддержкой виртуальной файловой системы (VFS). Реализованы этапы 1-3:

1. **Этап 1**: Базовая оболочка с командной строкой
2. **Этап 2**: Поддержка параметров командной строки и стартовых скриптов  
3. **Этап 3**: Виртуальная файловая система (VFS) с поддержкой JSON

## Возможности

### Параметры командной строки

- `--vfs PATH` - Путь к файлу виртуальной файловой системы (JSON формат)
- `--script PATH` - Путь к стартовому скрипту для выполнения команд
- `--interactive` - Входить в интерактивный режим после выполнения стартового скрипта
- `--demo` - Запустить демо-режим (унаследовано с этапа 1)
- `--help` - Показать справку

### Поддерживаемые команды в эмуляторе

**Навигация и просмотр:**
- `ls [path]` - Показать содержимое директории
- `cd [path]` - Изменить текущую директорию
- `pwd` - Показать текущую директорию
- `cat <file>` - Показать содержимое файла

**Создание файлов и директорий:**
- `mkdir <dir>` - Создать директорию
- `touch <file>` - Создать пустой файл

**Работа с VFS:**
- `vfs-save <path>` - Сохранить текущее состояние VFS в JSON файл

**Система:**
- `exit` - Завершить работу эмулятора

### Виртуальная файловая система (VFS)

- Все операции выполняются в памяти
- Загрузка из JSON файлов
- Поддержка текстовых файлов и бинарных данных (base64)
- Поддержка вложенных директорий любой глубины
- Сохранение состояния VFS в JSON формат

### Стартовые скрипты

Стартовые скрипты поддерживают:
- Комментарии (строки, начинающиеся с `#`)
- Выполнение команд эмулятора
- Отображение как ввода, так и вывода для имитации диалога с пользователем

### Отладочный вывод

При запуске эмулятор выводит все заданные параметры конфигурации.

## Структура проекта

```
unix-console-emulator-practice/
├── main.py                      # Основной файл эмулятора
├── README.md                   # Документация проекта  
└── tests/                      # Тесты, VFS файлы и примеры
    ├── README.md              # Документация тестов
    ├── startup_basic.sh        # Простой стартовый скрипт
    ├── startup_full_test.sh    # Полный тест всех команд
    ├── vfs_minimal.json        # Минимальная VFS (1 файл)
    ├── vfs_multifile.json      # VFS с несколькими файлами  
    ├── vfs_complex.json        # Сложная VFS (3+ уровня)
    ├── test_basic.bat         # Базовый тест (Windows CMD)
    ├── test_basic.ps1         # Базовый тест (PowerShell)
    ├── test_vfs_minimal.bat   # Тест минимальной VFS
    ├── test_vfs_multifile.bat # Тест VFS с несколькими файлами
    ├── test_vfs_complex.bat   # Тест сложной VFS
    └── test_vfs_all.ps1       # Тест всех VFS (PowerShell)
```

## Файлы проекта

### Основные файлы
- `main.py` - Основной файл эмулятора с полной поддержкой VFS и команд
- `tests/startup_basic.sh` - Простой стартовый скрипт для демонстрации
- `tests/startup_full_test.sh` - Полный тест всех реализованных команд

### VFS файлы
- `tests/vfs_minimal.json` - Минимальная VFS с одним файлом
- `tests/vfs_multifile.json` - VFS с несколькими файлами разных типов
- `tests/vfs_complex.json` - Сложная VFS с глубокой структурой каталогов (3+ уровня)

### Тестовые файлы
- `tests/test_basic.bat` - Простой тест для Windows CMD
- `tests/test_basic.ps1` - Простой тест для PowerShell
- `tests/test_vfs_minimal.bat` - Тест минимальной VFS
- `tests/test_vfs_multifile.bat` - Тест VFS с несколькими файлами
- `tests/test_vfs_complex.bat` - Тест сложной VFS структуры
- `tests/test_vfs_all.ps1` - Комплексный тест всех VFS## Использование

### Основные команды запуска

**Интерактивный режим (по умолчанию):**
```bash
python main.py
```

**С виртуальной файловой системой:**
```bash
python main.py --vfs tests/vfs_minimal.json
python main.py --vfs tests/vfs_multifile.json  
python main.py --vfs tests/vfs_complex.json
```

**Выполнение стартового скрипта:**
```bash
python main.py --script tests/startup_basic.sh
python main.py --script tests/startup_full_test.sh
```

**VFS + стартовый скрипт:**
```bash
python main.py --vfs tests/vfs_minimal.json --script tests/startup_basic.sh
python main.py --vfs tests/vfs_complex.json --script tests/startup_full_test.sh
```

**VFS + скрипт + интерактивный режим:**
```bash
python main.py --vfs tests/vfs_complex.json --script tests/startup_basic.sh --interactive
```

**Демо-режим:**
```bash
python main.py --demo
```

**Справка:**
```bash
python main.py --help
```

### Команды внутри эмулятора

**Навигация:**
```bash
pwd                    # Показать текущую директорию
ls                     # Показать содержимое текущей директории
ls /home/user         # Показать содержимое указанной директории
cd /home              # Перейти в директорию
cd ..                 # Перейти на уровень выше
cd /                  # Перейти в корень
```

**Просмотр файлов:**
```bash
cat filename.txt      # Показать содержимое файла
cat /home/user/file.txt # Показать файл по абсолютному пути
```

**Создание:**
```bash
mkdir new_directory   # Создать директорию
touch new_file.txt    # Создать пустой файл
```

**Работа с VFS:**
```bash
vfs-save backup.json  # Сохранить текущее состояние VFS
```

# UNIX Console Emulator

Эмулятор командной строки UNIX с поддержкой виртуальной файловой системы (VFS), скриптов запуска и тестовых сценариев.

## Основные команды

- `ls` — показать содержимое директории
- `cd <dir>` — перейти в директорию
- `pwd` — показать текущий путь
- `cat <file>` — вывести содержимое файла
- `mkdir <dir>` — создать директорию
- `touch <file>` — создать пустой файл
- `vfs-save <file>` — сохранить VFS в файл
- `exit` — выйти из эмулятора

## Запуск

```bash
python main.py --help                # Справка
python main.py --interactive         # Интерактивный режим
python main.py --vfs <vfs.json>      # Загрузка VFS
python main.py --script <script.sh>  # Запуск скрипта
python main.py --vfs <vfs.json> --script <script.sh>
```

## Тесты

Все тестовые скрипты и VFS-файлы находятся в папке `tests`.

### Запуск базовых тестов

Windows CMD:
```cmd
cd tests && test_basic.bat
```
PowerShell:
```powershell
cd tests; .\test_basic.ps1
```

### Запуск тестов VFS

Windows CMD:
```cmd
cd tests && test_vfs_minimal.bat
cd tests && test_vfs_multifile.bat
cd tests && test_vfs_complex.bat
```
PowerShell:
```powershell
cd tests; .\test_vfs_all.ps1
```

## Формат VFS

VFS — это JSON-структура с директориями и файлами:

```json
{
  "/": {"type": "directory", "children": {"file.txt": "/file.txt"}},
  "/file.txt": {"type": "file", "content": "Hello", "encoding": "text"}
}
```

Бинарные файлы используют encoding: "base64".

## Пример стартового скрипта

```bash
# Проверка команд
ls
cd /home
ls
exit
```

## Статус

- Все требования этапов 1–3 реализованы: интерактив, параметры, VFS, тесты, документация.