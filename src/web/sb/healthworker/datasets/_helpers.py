import csv
import json
import os.path

def read_csv(path, fields=None):
  items = []
  with open(path, 'rU') as f:
    reader = csv.DictReader(f, fieldnames=fields)
    items = list(reader)
  return items

# Read LF terminated json
def read_lf_json(path):
  with open(path, 'r') as f:
    data = f.readlines()
  return [json.loads(line) for line in data]

def get_path(*path_parts):
  return os.path.join(os.path.split(__file__)[0], *path_parts)

# Helper to return first record of a QuerySet
def first(qs):
  r = list(qs[:1])
  if r:
    return r[0]
  return None

