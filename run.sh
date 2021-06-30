#!/bin/bash
export TENSORFLOW_MODEL_DIR=/mnt/localscratch/maastro/Leroy/bodycomposition/logs/gradient_tape/stability_new_params_contour/20210529-084544/saved_models/model_26200
export TENSORFLOW_PARAMS_FILE=/mnt/localscratch/maastro/Leroy/bodycomposition/logs/gradient_tape/stability_new_params_contour/20210529-084544/params.json
docker-compose up -d; docker-compose logs -f
