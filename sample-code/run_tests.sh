#!/bin/bash

# Validate the number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <chart_dir> <values_file>"
    exit 1
fi

CHART_DIR=$1
VALUES_FILE=$2

# Execute the Python script for rendering
python renderer.py "$CHART_DIR" "$VALUES_FILE"

# Check if the Python script executed successfully
if [ $? -eq 0 ]; then
    RENDERED_CHART_DIR="${CHART_DIR}_rendered"
    echo "Rendering completed successfully. Running Helm unittest..."
    helm unittest "$RENDERED_CHART_DIR"
    if [ $? -eq 0 ]; then
        echo "Helm unittests passed successfully."
        rm -rf "$RENDERED_CHART_DIR"
        echo "Cleaned up rendered directory."
    else
        echo "Helm unittests failed. Check the rendered files at $RENDERED_CHART_DIR for debugging."
    fi
else
    echo "Rendering failed. Please check the output for errors."
fi
