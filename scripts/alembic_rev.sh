#!/usr/bin/env bash

alembic revision --autogenerate -m "$1"
alembic upgrade head
git add migrations/versions