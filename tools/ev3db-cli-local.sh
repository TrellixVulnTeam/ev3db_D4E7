#!/usr/bin/env bash
set -e
dir=$(dirname "$(dirname "$0")")
"$dir"/ev3db-cli -u http://127.0.0.1:55555 "$@"
