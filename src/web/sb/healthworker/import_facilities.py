import fileinput
import json

import django
from django.db import transaction

from sb.healthworker import models

def import_facility(f):
  tz = get_or_create_region_by_title_type("TZ", "Country", None)
  district = get_or_create_region_by_title_type(f["district"], "District", tz)
  division = get_or_create_region_by_title_type(f["division"], "Division", district)
  ward = get_or_create_region_by_title_type(f["ward"], "Ward", division)
  facility = models.Facility()
  facility.region = get_or_create_region_by_title_type(f["village"], "Village", ward)
  facility.title = f["fname"]
  facility.serial_number = f["sn"]
  facility.place_type = f["place"]
  facility.ownership_type = f["owner2"]
  facility.owner = f["owner"]
  facility.address = f["mitaa"]
  facility.type = models.get_or_create_by_title(models.FacilityType, f["ftype"])
  facility.save()
  print "added ", facility

def main():
  with transaction.commit_on_success():
    fields = []
    for idx, line in enumerate(fileinput.input()):
      values = line.decode('utf-8').rstrip('\n').split('\t')
      if idx == 0:
        fields = [i.lower() for i in values]
      else:
        f = dict(zip(fields, values))
        print f
        if f.get('fname'):
          import_facility(f)

if __name__ == '__main__':
  main()


