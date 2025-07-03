#!/bin/bash

PROJECT_DIR="Repeater"

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--directory)
            PROJECT_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter passed: $1"
            exit 1
            ;;
    esac
done

cd "$(dirname "$0")/$PROJECT_DIR" || {
    echo "Could not change directory to $PROJECT_DIR"
    exit 1
}
./venv/bin/nb run --reload

read -p "Press enter to exit"