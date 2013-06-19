import datetime
import os.path

from django.db import models
from django.db import transaction
from south.db import db
from south.v2 import SchemaMigration

from sb.healthworker import models
from sb.testing import is_testing
import sb.healthworker

from sb.healthworker.datasets import _helpers

def run():
  pkg_dir = os.path.split(sb.healthworker.__file__)[0]
  specialties_txt = _helpers.get_path('specialties.txt')
  fields = []
  cadre = None
  specialty = None
  parent = None
  with transaction.commit_on_success():
    for idx, line in enumerate(open(specialties_txt, 'r')):
      line = line.decode('utf-8').rstrip('\n')
      values = line.split('\t')
      if idx == 0:
        fields = [i.lower() for i in values]
      else:
        item = dict(zip(fields, values))
        if item['cadre']:
          cadre = models.Specialty()
          cadre.abbreviation = item['cadre abbreviation']
          cadre.title = item['cadre']
          cadre.save()
          specialty = None

        if item['specialty']:
          specialty = models.Specialty()
          specialty.title = item['specialty']
          assert cadre is not None
          specialty.parent_specialty = cadre
          specialty.save()

        if item['super specialty']:
          super_specialty = models.Specialty()
          super_specialty.title = item['super specialty']
          assert specialty is not None
          super_specialty.parent_specialty = specialty
          super_specialty.save()

