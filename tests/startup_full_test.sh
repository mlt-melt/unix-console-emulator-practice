# Полный тестовый скрипт для UNIX Console Emulator
# Демонстрирует все реализованные команды и работу с VFS

# Проверим текущую директорию
pwd
ls

# Перейдем в корень и посмотрим содержимое
cd /
pwd
ls

# Попробуем перейти в существующий каталог
cd home
pwd
ls

# Перейдем глубже по структуре каталогов
cd user/documents
pwd
ls

# Посмотрим содержимое файлов
cat readme.md
cat ../profile.txt

# Перейдем в рабочую директорию и посмотрим проект
cd work/project1
pwd
ls
cat main.py
cat data.json

# Протестируем команды создания файлов и директорий
mkdir test_dir
touch test_file.txt
ls

# Попробуем сохранить текущее состояние VFS
vfs-save /tmp/current_vfs.json

# Вернемся в корень и проверим другие пути
cd /
ls usr
ls usr/bin
cat usr/bin/python

# Посмотрим на бинарный файл (base64)
cd usr/lib
ls
cat libtest.so

# Протестируем обработку ошибок
cat nonexistent_file.txt
cd nonexistent_directory
ls nonexistent_path

# Тестируем неизвестные команды
unknown_command arg1 arg2
invalid_cmd

# Вернемся в начальную директорию
cd /
pwd

# Завершим тестирование
exit