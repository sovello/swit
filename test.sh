#!/bin/bash
# Run the tests
export PYTHONPATH=src/web
export TESTING=1
python src/web/manage.py test --noinput healthworker

