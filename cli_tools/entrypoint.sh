#!/bin/sh
set -e

# Copy config files to $HOME
cp -r /retriever/cli_tools/.pgpass.conf  ~/
cp -r /retriever/cli_tools/.my.cnf  ~/

exec "$@"
