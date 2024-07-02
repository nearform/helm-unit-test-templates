import os
import sys
from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader
import json

def load_params(file_path):
    """ Load parameters from a JSON file. """
    with open(file_path, 'r') as file:
        return json.load(file)

def render_templates(source_dir, dest_dir, params):
    """ Render Jinja2 templates, replacing placeholders and changing file extensions to .yaml """
    env = Environment(loader=FileSystemLoader(source_dir), trim_blocks=True, lstrip_blocks=True)
    for file_path in source_dir.rglob('*.j2'):
        template = env.get_template(str(file_path.relative_to(source_dir)))
        rendered_content = template.render(params)
        new_file_path = file_path.with_suffix('.yaml')
        new_file_path.write_text(rendered_content)
        print(f"Rendered and saved {new_file_path}")
        file_path.unlink()

def main(chart_dir, values_file):
    chart_dir = Path(chart_dir)
    rendered_chart_dir = chart_dir.parent / (chart_dir.name + "_rendered")

    params = load_params(values_file)
    print("Loaded parameters:", params)

    if rendered_chart_dir.exists():
        shutil.rmtree(rendered_chart_dir)
    shutil.copytree(chart_dir, rendered_chart_dir)
    print(f"Copied {chart_dir} to {rendered_chart_dir}")

    render_templates(rendered_chart_dir, rendered_chart_dir, params)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python render_and_test.py <chart_dir> <values_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])




# import os
# import sys
# import shutil
# from jinja2 import Environment, FileSystemLoader
# import json

# def load_params(file_path):
#     """ Load parameters from a JSON file. """
#     with open(file_path, 'r') as file:
#         return json.load(file)

# def render_templates(source_dir, dest_dir, params):
#     """ Render Jinja2 templates, replacing placeholders and changing file extensions to .yaml """
#     env = Environment(loader=FileSystemLoader(source_dir), trim_blocks=True, lstrip_blocks=True)
    
#     # Iterate over all files in the source directory
#     for root, dirs, files in os.walk(source_dir):
#         for file_name in files:
#             if file_name.endswith('.j2'):
#                 # Setup full file paths
#                 full_file_path = os.path.join(root, file_name)
#                 template = env.get_template(os.path.relpath(full_file_path, start=source_dir))
#                 rendered_content = template.render(params)
                
#                 # Correctly create new file name and path by replacing .j2 with .yaml
#                 new_file_name = file_name[:-3] + '.yaml'  # Removes the last 3 characters (.j2) and adds .yaml
#                 new_file_path = os.path.join(root, new_file_name)
                
#                 # Save rendered content to new file
#                 with open(new_file_path, 'w') as new_file:
#                     new_file.write(rendered_content)
#                 print(f"Rendered and saved {new_file_path}")

#                 # Optionally remove the original .j2 file
#                 os.remove(full_file_path)


# def main(chart_dir, rendered_chart_dir, values_file):
#     # chart_dir = 'mars'
#     # values_file = 'values.json'
#     # rendered_chart_dir = 'rendered_mars'

#     # Load parameters
#     params = load_params(values_file)
#     print("Loaded parameters:", params)

#     # Copy the entire Helm chart directory
#     if os.path.exists(rendered_chart_dir):
#         shutil.rmtree(rendered_chart_dir)
#     shutil.copytree(chart_dir, rendered_chart_dir)
#     print(f"Copied {chart_dir} to {rendered_chart_dir}")

#     # Render test files located in the tests directory of the rendered chart
#     tests_dir = os.path.join(rendered_chart_dir, 'tests')
#     render_templates(tests_dir, tests_dir, params)

#     # # Run Helm unittest
#     # print("Running Helm unittest...")
#     # os.system(f"helm unittest {rendered_chart_dir}")

# # if __name__ == "__main__":
# #     main()

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python render_and_test.py <chart_dir> <rendered_chart_dir> <values_file>")
#         sys.exit(1)
#     main(sys.argv[1], sys.argv[2], sys.argv[3])