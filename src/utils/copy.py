
import os

def copy_from_to(src_dir, dest_dir):
  # Write a recursive function that copies all contents from a src directory to a destination directory

  # 1 - Delete ALL contents of the destination directory
  # 2 - Copy all the files and subdirectories, nested files, etc
  # 3 - Log the path of each file you copy so you can see what's happening as you run and debug the code

  # 4 - Hook the function up to your main function and test it
  # 5 - Add the public/ directory to your .gitignore file

  '''Useful Standard Library Docs

  os.path.exists(path):
    Returns True if the path refers to an existing path or an open file descriptor
    
    Returns False for broken symbolic links

  os.listdir(path='.'):
    Return a list containing the names of the entries in the directory given by path.  The list is in arbitrary order, and does not include the special entries '.' and '..' even if they are present in the directory.

    path may be a path-like object.

  os.path.join(path, *paths):
    Join one or more path segments.  The return value is the concatenation of path and all members of *paths, with exactly one directory separator following each non-empty part, excepth the last.

    os.path.join("c:", "foo") represents a path relative to the current directory on drive C: (c:foo), not c:\foo

  os.path.isfile(path):
    Return True if path is an existing regular file.

  os.mkdir(path, mode=0o777, *, dir_fd = None):
    Create a directory named path with numeric mode mode
    
    If the directory already exists FileExistsError is raised.

    If a parent directory in the path does not exist, FileNotFoundError is raised

  
  shutil.copy(src, dst, *, follow_symlinks=True):
    Copies the file src to the file or directory dst.

    Src and dst should be path-like objects or strings.

    If dst specifies a directory, the file will be copied into dst using the base filename from src

    If dst specifies a file that already exists, it will be replaced.

    Returns the path to the newly created file

  shuitl.rmtree(path, ignore_errors=False, onerror=None, *, onexc=None, dir_fd = None):
    Delete an entire directory tree - path must point to a directory

    If ignore_errors is true, errors resulting from failed removals will be ignored
  '''
  # Check if destination path exists:

  if os.path.exists(dest_dir):
    print("Destination Folder Contents\n", os.listdir(dest_dir))
  else:
    # Use os.path.join to create the path to the destination dir
    # Use os.mkdir() to create the directory
    pass

  
  # Return a list of all entries in the src_dir
  print(os.listdir(src_dir))
