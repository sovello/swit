import os.path
import re

from django.db import transaction
from south.v2 import SchemaMigration

from sb.healthworker import models
from sb.util import safe, read_tsv

district_stem_pat = re.compile(r'\s+(?:disrict|district|mc|dc|cc)$', re.I)

def stem_tz_district_name(name):
  if name:
    return district_stem_pat.sub('', name).strip()
  else:
    return ''

def import_facility(f):
  region = models.Region.get_or_create_region_by_title_type("TZ", "Country", None)
  if f["region name"]:
    region = models.Region.get_or_create_region_by_title_type(f["region name"], "Region", region)
    if f["district (central government)"]:
      region = models.Region.get_or_create_region_by_title_type(stem_tz_district_name(f["district (central government)"]), "District", region)
      if f["division"]:
        region = models.Region.get_or_create_region_by_title_type(f["division"], "Division", region)
        if f["ward"]:
          region = models.Region.get_or_create_region_by_title_type(f["ward"], "Ward", region)
          if f["village/street"]:
            region = models.Region.get_or_create_region_by_title_type(f["village/street"], "Village", region)

  facility = models.Facility()
  facility.region = region
  facility.title = f["name"]
  facility.serial_number = f["sn"]
  facility.ownership_type = f["ownership"]
  facility.owner = f["ownership detail"]
  facility.hmis = f["hmis (msimbo)"]
  facility.remarks = f["remarks"]
  facility.alternative_names = f["alternative name(s)"]
  facility.source = f["source"]
  facility.latitude = safe(lambda: float(f["latitude"]))
  facility.longitude = safe(lambda: float(f["longitude"]))
  if f["hf type"]:
    facility.type = models.get_or_create_by_title(models.FacilityType, f["hf type"])
  facility.registration_num = f["registration no."]
  facility.status = f["status"]
  facility.current_id = f["current id"]
  facility.is_user_submitted = False
  facility.save()

def import_facilities():
  facilities_txt = os.path.join(os.path.split(__file__)[0], 'facilities-01-18-2013.txt')
  for item in list(read_tsv(facilities_txt))[:500]:
    #if item.get('name'):
    import_facility(item)

def delete_regions():
  models.Region.objects.all().delete()

def delete_facilities():
  models.FacilityType.objects.all().delete()
  models.Facility.objects.all().delete()

class Migration(SchemaMigration):
    def forwards(self, orm):
      with transaction.commit_on_success():
        delete_regions()
        delete_facilities()
        import_facilities()

    def backwards(self, orm):
      pass

