# Sample Code for helm-unit-test-templates

## Description

This directory contains sample code and scripts to demonstrate the usage of helm-unit-test-templates.

## Structure

- `mars/`: Sample Helm chart
- `renderer.py`: Python script for rendering templates
- `run_tests.sh`: Shell script to run the tests
- `values.json`: Sample values file for customization

## How to Use

1. Ensure you have Helm and the helm-unittest plugin installed.

2. To use the Renderer script and run against templated test suites:

   a. Review and modify the `values.json` file if needed with your specific parameters:
      ```json
      {
        "CHART_NAME": "mars",
        "RELEASE_NAME": "foobar",
        "CONFIGMAP_DATA": {
          "TZ": "UTC",
          "LOG_LEVEL": "INFO"
        }
      }
      ```

   b. Run the template rendering script:
      ```
      ./run_tests.sh mars values.json
      ```

## What Happens When You Run the Script

1. `run_tests.sh` calls `renderer.py` with the chart directory and values file.
2. `renderer.py` creates the `mars_rendered` directory, cloning the original chart.
3. It processes YAML files in `mars/tests/`, applying Jinja2 templating with values from `values.json`.
4. Rendered test files are saved in `mars_rendered/tests/`.
5. Helm unit tests run against the rendered chart.
6. The `mars_rendered` directory is cleaned up if tests pass, or left for debugging if they fail.

## Customizing Tests

- Modify YAML test templates in `mars/tests/` to add or change test scenarios.
- Adjust `values.json` to customize tests for the chart.
- For more advanced customizations, you may need to modify `renderer.py`.
