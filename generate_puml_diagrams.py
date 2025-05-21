import os
import subprocess

# set the root directory to start searching for .puml files
root_dir = '.'

# walk through all directories and files starting from root_dir
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # only process files that end with .puml (plantuml files)
        if filename.endswith('.puml'):
            puml_path = os.path.join(dirpath, filename)
            print(f"Generating diagram for {puml_path}")
            try:
                # run plantuml to generate a png diagram from the .puml file
                subprocess.run(['plantuml', '-tpng', puml_path], check=True)
            except subprocess.CalledProcessError as e:
                # print an error message if diagram generation fails
                print(f"Error generating diagram for {puml_path}: {e}") 