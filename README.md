# helm-unit-test-templates

Blueprint unit test templates for Helm charts

## Overview

This repository contains blueprint unit test templates and a customization script for Helm charts, designed to streamline the development process and ensure consistent quality across projects. It uses the [helm-unittest](https://github.com/helm-unittest/helm-unittest) framework for testing Helm charts.

## Features

- Blueprint unit test templates for common Helm chart scenarios
- Python script for template customization
- Support for various Kubernetes objects (ConfigMap, Secret, Deployment, Service)
- Easy adaptation to different chart names and configurations

## Prerequisites

- Python 3.9+
- Helm 3+
- helm-unittest plugin

## Quick Start

For detailed instructions on how to use these templates and run tests, please see the [sample code README](./sample-code/README.md).

## Repository Structure

- `sample-code/`: Contains example Helm chart and usage instructions
  - `mars/`: Sample Helm chart
  - `mars_rendered/`: Rendered version of the sample chart (generated during testing)
  - `README.md`: Detailed instructions for using the sample code
  - `renderer.py`: Python script for rendering templates
  - `run_tests.sh`: Shell script to run the tests
  - `values.json`: Sample values file for customization
