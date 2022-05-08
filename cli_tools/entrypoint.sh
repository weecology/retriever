#!/bin/sh
set -e

# Copy config files to $HOME
cp -r cli_tools/.pgpass  ~/
cp -r cli_tools/.my.cnf  ~/

exec "$@"
