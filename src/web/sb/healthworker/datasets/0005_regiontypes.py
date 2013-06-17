import os.path

from django.db import transaction
from south.v2 import SchemaMigration

from sb.healthworker import models

def add_region_types():
  models.get_or_create_by_title(models.RegionType, models.RegionType.COUNTRY)
  models.get_or_create_by_title(models.RegionType, models.RegionType.DIVISION)
  models.get_or_create_by_title(models.RegionType, models.RegionType.DISTRICT)
  models.get_or_create_by_title(models.RegionType, models.RegionType.VILLAGE)
  models.get_or_create_by_title(models.RegionType, models.RegionType.WARD)

class Migration(SchemaMigration):

    def forwards(self, orm):
      with transaction.commit_on_success():
        add_region_types()

    def backwards(self, orm):
      pass


