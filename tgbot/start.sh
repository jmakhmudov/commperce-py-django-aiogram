#!/usr/bin/env sh

set -o errexit
set -o nounset

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000