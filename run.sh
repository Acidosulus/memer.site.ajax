#!/bin/bash

cd /home/acidos/voc/memer.site

#tmux new-session -d -s mongo '/home/acidos/voc/memer.site/run_docker_compose_mongodb.sh' &

#tmux new-session -d -s postgres '/home/acidos/voc/memer.site/run_docker_compose_postgres.sh' &

#tmux new-session -d -s rabbit '/home/acidos/voc/memer.site/run_docker_compose_rabbitmq.sh' &

tmux new-session -d -s API '/home/acidos/voc/memer.site/APIServer/run_FastAPI_server.sh' &

tmux new-session -d -s Django '/home/acidos/voc/memer.site/voc/run_server.sh' &

tmux new-session -d -s MessageServer '/home/acidos/voc/memer.site/MessageLogServer/MessageLogServer.sh' &
