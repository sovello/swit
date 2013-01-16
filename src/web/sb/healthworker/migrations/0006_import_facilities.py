import os.path

from django.db import transaction
from south.v2 import SchemaMigration

from sb.healthworker import models

def import_facility(f):
  tz = models.Region.get_or_create_region_by_title_type("TZ", "Country")
  district = models.Region.get_or_create_region_by_title_type(f["district"], "District", tz)
  division = models.Region.get_or_create_region_by_title_type(f["division"], "Division", district)
  ward = models.Region.get_or_create_region_by_title_type(f["ward"], "Ward", division)
  facility = models.Facility()
  facility.region = models.Region.get_or_create_region_by_title_type(f["village"], "Village", ward)
  facility.title = f["fname"]
  facility.serial_number = f["sn"]
  facility.place_type = f["place"]
  facility.ownership_type = f["owner2"]
  facility.owner = f["owner"]
  facility.address = f["mitaa"]
  facility.type = models.get_or_create_by_title(models.FacilityType, f["ftype"])
  facility.save()
  print "added ", facility

def import_facilities():
  fields = []
  facilities_txt = os.path.join(
      os.path.split(__file__)[0],
      'facilities.txt')

  for idx, line in enumerate(open(facilities_txt, 'r')):
    values = line.decode('utf-8').rstrip('\n').split('\t')
    if idx == 0:
      fields = [i.lower() for i in values]
    else:
      f = dict(zip(fields, values))
      print f
      if f.get('fname'):
        import_facility(f)

class Migration(SchemaMigration):
    def forwards(self, orm):
      with transaction.commit_on_success():
        import_facilities()

    def backwards(self, orm):
      pass

