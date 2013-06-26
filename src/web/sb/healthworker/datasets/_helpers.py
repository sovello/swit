import csv
import os.path


def read_csv(path, fields=None):
  items = []
  with open(path, 'rU') as f:
    reader = csv.DictReader(f, fieldnames=fields)
    items = list(reader)
  return items

def get_path(*path_parts):
  return os.path.join(os.path.split(__file__)[0], *path_parts)

