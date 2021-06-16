#!/bin/bash
# shellcheck disable=SC2164
cd l3autoseg
# options: default high low --burst
python manage.py rqworker default
