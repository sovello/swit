import os.path

def get_path(*path_parts):
  return os.path.join(os.path.split(__file__)[0], *path_parts)
