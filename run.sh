#!/bin/bash

PROJECT="Repeater"

echo "\033]2;$PROJECT\007"

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--directory)
            PROJECT="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter passed: $1"
            exit 1
            ;;
    esac
done

cd "$(dirname "$0")/$PROJECT_DIR" || {
    echo "Could not change directory to $PROJECT"
    exit 1
}
./venv/bin/nb run

read -p "Press enter to exit"