import os
import os.path
import re

from django.db import transaction

from sb.healthworker import models

_dataset_dir = os.path.join(os.path.split(__file__)[0], "datasets")

_module_pattern = re.compile(r"^([^_]\w+)[.]py$")

def get_datasets():
  paths = os.listdir(_dataset_dir)
  matches = filter(None, map(_module_pattern.match, paths))
  modules = map(lambda i: i.group(1), matches)
  return modules

def _import(path):
  return reduce(getattr, path.split(".")[1:], __import__(path))

def import_all_datasets():
  datasets = get_datasets()
  # FIXME: add natural sort
  datasets.sort()
  for dataset in datasets:
    if not models.DataSet.objects.filter(key=dataset).count():
      module = _import("sb.healthworker.datasets." + dataset)
      module.run()
      row = models.DataSet()
      row.key = dataset
      row.save()

