import os.path

from django.db import transaction
from south.v2 import SchemaMigration

from sb.healthworker import models

def import_districts():
  tz = models.Region.get_or_create_region_by_title_type('TZ', 'Country')
  districts_txt = os.path.join(
      os.path.split(__file__)[0],
      'districts.txt')
  region = None
  for idx, line in enumerate(open(districts_txt, 'r')):
    if idx == 0:
      continue
    line = line.rstrip()
    if ',' not in line:
      continue
    region_title, district_title = line.split(',')
    if region_title:
      region = models.Region.get_or_create_region_by_title_type(region_title, 'Region', parent=tz)
    assert region
    models.Region.get_or_create_region_by_title_type(district_title, 'District', parent=region)

class Migration(SchemaMigration):

    def forwards(self, orm):
      with transaction.commit_on_success():
        import_districts()

    def backwards(self, orm):
      pass


