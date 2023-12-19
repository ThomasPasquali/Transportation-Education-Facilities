import os

def concatenate_files(folder_path, output_file):
  all_files = []

  # Iterate through all files in the folder and its subfolders
  for folder_name, _, files in os.walk(folder_path):
    for file_name in files:
      file_path = os.path.join(folder_name, file_name)
      all_files.append(file_path)

  print('All files: ', all_files)

  with open(output_file, 'w') as output:
    # Iterate through each file path and append its content to the output file
    for file_path in all_files:
      with open(file_path, 'r') as input_file:
        output.write(input_file.read())
        output.write('\n')

  print(f"All files in {folder_path} and its subfolders have been appended to {output_file}")


folder_path = './Karma RDF'
output_file = './KG.ttl'
concatenate_files(folder_path, output_file)