#!/usr/bin/env bash
# Missouri Driver Guide - Launcher Script

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "Launching Missouri Driver Guide Interactive Web Server..."
python3 server.py --open
