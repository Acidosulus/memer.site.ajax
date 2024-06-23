@echo off
setlocal

REM ��⠭���� ��ࠬ���� ������祭�� � ��襩 ���� ������ PostgreSQL
set PGUSER=postgres
set PGPASSWORD=321
set PGHOST=192.168.0.112
set PGPORT=5432
set DATABASE=language

REM ����, ��� ���� ��࠭��� १�ࢭ� �����
set BACKUP_DIR=G:\backup\posgreesql

REM �������� ��⠫��� ��� १�ࢭ�� �����, �᫨ �� �� �������
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM ��ନ஢���� ����� 䠩�� १�ࢭ�� ����� �� �᭮�� ⥪�饩 ���� � �६���
set TIMESTAMP=%DATE:/=-%_%TIME::=-%
set TIMESTAMP=%TIMESTAMP: =0%
set TIMESTAMP=%TIMESTAMP:~0,19%
set FILENAME=%BACKUP_DIR%\backup_%DATABASE%_%TIMESTAMP%.sql

REM ������� pg_dump ��� ᮧ����� १�ࢭ�� ����� ⮫쪮 �奬� "language"
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" --username=%PGUSER% --host=%PGHOST% --port=%PGPORT% --dbname=%DATABASE% > "%FILENAME%"

REM �஢�ઠ �ᯥ譮�� �믮������ १�ࢭ��� ����஢����
if %ERRORLEVEL% neq 0 (
  echo �訡��: �� 㤠���� ᮧ���� १�ࢭ�� ����� ��� ������.
  exit /b %ERRORLEVEL%
) else (
  echo ����ࢭ�� ����� �ᯥ譮 ᮧ����: %FILENAME%
)

endlocal