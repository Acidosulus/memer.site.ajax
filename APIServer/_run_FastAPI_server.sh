#!/bin/sh

# Путь к каталогу с виртуальным окружением
VENV_PATH="/home/acidos/voc/memer.site/APIServer/venv"

# Активируем виртуальное окружение
source "$VENV_PATH/bin/activate"

# Переходим в каталог с кодом сервера
cd /home/acidos/voc/memer.site/APIServer

# Запускаем FastAPI сервер
uvicorn APIServer:app --reload --host 0.0.0.0 --port 9001
