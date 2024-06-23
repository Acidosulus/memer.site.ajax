#!/bin/bash

cd /home/acidos/voc/memer.site

tmux new-window -n all_sessions
tmux split-window -h
tmux select-pane -t 0
tmux attach-session -t mongo

tmux select-pane -t 1
tmux attach-session -t postgres

tmux select-pane -t 2
tmux attach-session -t rabbit

tmux select-pane -t 3
tmux attach-session -t API

tmux select-pane -t 4
tmux attach-session -t Django

tmux select-pane -t 5
tmux attach-session -t MessageServer

tmux select-pane -t 0

tmux -4 attach-session -d
