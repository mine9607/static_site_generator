
import os
import shutil

def copy_from_to(src_dir, dest_dir):
  # Write a recursive function that copies all contents from a src directory to a destination directory

  # create absolute paths to the src and dest locations
  src_path = os.path.abspath(src_dir)
  dest_path = os.path.abspath(dest_dir)

  # Check if the src dir exists
  if not os.path.exists(src_path):
      raise Exception(f"Directory {src_path} could not be found please check path")

  # If dest dir exists delete it and its contents
  if os.path.exists(dest_path):
      shutil.rmtree(dest_path)

  # Create a new dest_dir
  try:
      os.mkdir(dest_path)
      print(f"Directory {dest_path} created successfully.")
  except Exception as e:
      print(f"Failed to create directory at {dest_path}: {e}")
      raise

  # Create a list of contents in the src dir
  src_contents = os.listdir(src_dir)

  # If the directory is empty then return
  if len(src_contents) == 0:
      return

  for item in src_contents:
      # create a path to the item
      item_src_path = os.path.join(src_path, item)
      item_dest_path = os.path.join(dest_path,item)

      # check if the item is a file
      if os.path.isfile(item_src_path):
          # copy the file to the dest_dir
          try:
              file_dest_path = shutil.copy(item_src_path, item_dest_path)
              # log the file name copied:
              print(f"Copied {item} to {file_dest_path} successfully")
          except Exception as e:
              print(f"An error occurred copying file {item} to {item_dest_path}: {e}")
              raise
    
      # for directories
      else:
        # create a new directory at item_dest_path
        try:
            os.mkdir(item_dest_path)
        except Exception as e:
            print(f"Failed to create directory {item} at {item_dest_path}: {e}")
            raise
        # recursively call the function using item_src_path
        copy_from_to(item_src_path, item_dest_path)

