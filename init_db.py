import os
import subprocess

root_dir = "."
db_name = "tpmixte"

def import_json_files(root_dir, db_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'data' in dirpath:
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)

                    collection_name = os.path.splitext(filename)[0]

                    command = [
                        "mongoimport",
                        "--db", db_name,
                        "--collection", collection_name,
                        "--file", file_path,
                        "--jsonArray"
                    ]

                    print(f"Importing {file_path} into collection {collection_name}...")
                    result = subprocess.run(command, capture_output=True, text=True)

                    if result.returncode == 0:
                        print(f"Successfully imported {file_path}")
                    else:
                        print(f"Error importing {file_path}: {result.stderr}")


import_json_files(root_dir, db_name)
