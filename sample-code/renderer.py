import sys
import json
from pathlib import Path
import shutil
from typing import Dict, Any
from jinja2 import Template
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_params(file_path: Path) -> Dict[str, Any]:
    """
    Load parameters from a JSON file.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        Dict[str, Any]: Loaded parameters.

    Raises:
        json.JSONDecodeError: If there's an error parsing the JSON file.
    """
    try:
        with file_path.open('r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file: {e}")
        raise

def render_yaml_template(content: str, params: Dict[str, Any]) -> str:
    """
    Render a YAML string as a Jinja2 template.

    Args:
        content (str): YAML content as a string.
        params (Dict[str, Any]): Parameters for rendering the template.

    Returns:
        str: Rendered YAML content.
    """
    template = Template(content)
    return template.render(params)

def process_test_yaml_files(source_dir: Path, dest_dir: Path, params: Dict[str, Any]) -> None:
    """
    Process YAML files in the Helm test folder, applying Jinja2 templating.

    Args:
        source_dir (Path): Directory containing the Helm chart.
        dest_dir (Path): Directory to save rendered YAML files.
        params (Dict[str, Any]): Parameters for rendering templates.
    """
    test_dir = source_dir / 'tests'
    rendered_test_dir = dest_dir / 'tests'

    if not test_dir.exists():
        logger.warning(f"Test directory not found: {test_dir}")
        return

    rendered_test_dir.mkdir(parents=True, exist_ok=True)

    for file_path in test_dir.glob('*.yaml'):
        try:
            with file_path.open('r') as file:
                content = file.read()
            
            rendered_content = render_yaml_template(content, params)
            
            # Validate the rendered content as YAML
            yaml.safe_load(rendered_content)
            
            dest_file_path = rendered_test_dir / file_path.name
            dest_file_path.write_text(rendered_content)
            logger.info(f"Processed and saved {dest_file_path}")
        except Exception as e:
            logger.error(f"Error processing YAML file {file_path}: {e}")

def main(chart_dir: Path, values_file: Path) -> None:
    """
    Main function to process Helm test YAML files and apply variable substitution.

    Args:
        chart_dir (Path): Directory containing the Helm chart.
        values_file (Path): File containing parameter values.
    """
    rendered_chart_dir = chart_dir.parent / (chart_dir.name + "_rendered")
    
    try:
        params = load_params(values_file)
        logger.info(f"Loaded parameters: {params}")

        if rendered_chart_dir.exists():
            shutil.rmtree(rendered_chart_dir)
        shutil.copytree(chart_dir, rendered_chart_dir)
        logger.info(f"Copied {chart_dir} to {rendered_chart_dir}")

        process_test_yaml_files(chart_dir, rendered_chart_dir, params)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.error("Usage: python3 render_helm_tests.py <chart_dir> <values_file>")
        sys.exit(1)
    
    main(Path(sys.argv[1]), Path(sys.argv[2]))