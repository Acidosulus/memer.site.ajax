#!/bin/bash

cd /home/acidos/voc/memer.site/voc
source /home/acidos/voc/memer.site/voc/venv/bin/activate
python3 manage.py runserver 0.0.0.0:13548
#uvicorn voc.asgi:application --reload --host 0.0.0.0 --port 9002
