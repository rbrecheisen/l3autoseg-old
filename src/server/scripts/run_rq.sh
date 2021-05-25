#!/usr/bin/env bash

source $HOME/.venv/l3autoseg/bin/activate

export DJANGO_SETTINGS_MODULE=server.settings
export SQLITE3_DIR=/tmp/l3autoseg

if [ "${1}" != "" ]; then
  export CUDA_VISIBLE_DEVICES=${1}
fi

rq worker --with-scheduler
