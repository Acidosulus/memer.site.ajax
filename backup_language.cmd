@echo off
setlocal

REM Установите параметры подключения к вашей базе данных PostgreSQL
set PGUSER=postgres
set PGPASSWORD=321
set PGHOST=192.168.0.112
set PGPORT=5432
set DATABASE=language

REM Путь, где будут сохранены резервные копии
set BACKUP_DIR=G:\backup\posgreesql

REM Создание каталога для резервных копий, если он не существует
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Формирование имени файла резервной копии на основе текущей даты и времени
set TIMESTAMP=%DATE:/=-%_%TIME::=-%
set TIMESTAMP=%TIMESTAMP: =0%
set TIMESTAMP=%TIMESTAMP:~0,19%
set FILENAME=%BACKUP_DIR%\backup_%DATABASE%_%TIMESTAMP%.sql

REM Команда pg_dump для создания резервной копии только схемы "language"
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" --username=%PGUSER% --host=%PGHOST% --port=%PGPORT% --dbname=%DATABASE% > "%FILENAME%"

REM Проверка успешности выполнения резервного копирования
if %ERRORLEVEL% neq 0 (
  echo Ошибка: Не удалось создать резервную копию баз данных.
  exit /b %ERRORLEVEL%
) else (
  echo Резервная копия успешно создана: %FILENAME%
)

endlocal