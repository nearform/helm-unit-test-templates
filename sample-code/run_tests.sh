#!/bin/bash

set -eu

# Validate the number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <chart_dir> <values_file>" >&2
    exit 1
fi

CHART_DIR="$1"
VALUES_FILE="$2"
RENDERED_CHART_DIR="${CHART_DIR}_rendered"

# Execute the Python script for rendering
if python renderer.py "$CHART_DIR" "$VALUES_FILE"; then
    echo "Rendering completed successfully. Running Helm unittest..."
    if helm unittest "$RENDERED_CHART_DIR"; then
        echo "Helm unittests passed successfully."
        echo "Cleaning up rendered directory."
        rm -rf "$RENDERED_CHART_DIR"
        echo "Cleaned up rendered directory."
    else
        echo "Helm unittests failed. Check the rendered files at $RENDERED_CHART_DIR for debugging." >&2
        exit 1
    fi
else
    echo "Rendering failed. Please check the output for errors." >&2
    exit 1
fi