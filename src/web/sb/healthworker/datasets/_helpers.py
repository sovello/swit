import csv
import os.path


def read_csv(path):
  items = []
  with open(path, 'r') as f:
    reader = csv.DictReader(f)
    items = list(reader)
  return items

def get_path(*path_parts):
  return os.path.join(os.path.split(__file__)[0], *path_parts)
