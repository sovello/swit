import os.path

from django.db import transaction
from south.v2 import SchemaMigration

from sb.healthworker import models
from sb.testing import is_testing

def import_facility(f):
  district = models.Region.get_or_create_region_by_title_type(f["district"], "District", None, filter_parent=False)
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

def add_region_district(i):
  tz = models.Region.get_or_create_region_by_title_type("TZ", "Country", None)
  region = models.Region.get_or_create_region_by_title_type(i['region'], "Region", tz)
  district = models.Region.get_or_create_region_by_title_type(i['district'], "District", region)

def read_tsv(path):
  fields = []
  for idx, line in enumerate(open(path, 'r')):
    line = line.decode('utf-8').rstrip('\r\n')
    vals = line.split('\t')
    if idx == 0:
      fields = vals
      fields = [f.lower() for f in fields]
    else:
      item = dict(zip(fields, vals))
      yield item

def import_regions():
  districts_txt = os.path.join(os.path.split(__file__)[0], 'districts.txt')
  for item in read_tsv(districts_txt):
    add_region_district(item)

def import_facilities():
  facilities_txt = os.path.join(os.path.split(__file__)[0], 'facilities.txt')
  for item in read_tsv(facilities_txt):
    if item.get('fname'):
      import_facility(item)

def delete_regions():
  models.Region.objects.all().delete()

def delete_facilities():
  models.Facility.objects.all().delete()

class Migration(SchemaMigration):
    def forwards(self, orm):
      if is_testing():
        return
      with transaction.commit_on_success():
        delete_regions()
        delete_facilities()
        import_regions()
        import_facilities()

    def backwards(self, orm):
      pass

