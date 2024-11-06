#!/bin/env bash

PROJECT=personal_journal
POSTGRES_VERSION=15 docker compose -p $PROJECT \
  --project-directory . \
  -f development/docker-compose.yml up
