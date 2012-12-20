import fileinput
import json

import django
from django.db import transaction

from sb.healthworker import models

def import_facility(f):
  facility = models.Facility()
  facility.town = f["town"]
  facility.title = f["title"]
  facility.owner = f["owner"]
  facility.ownership_type = f["ownership_type"]
  facility.address = f["address"]
  facility.phone = f["telephone"]
  facility.email = f["email"]
  facility.place_type = f["place_type"]
  if f["type"]:
    try:
      facility.type = models.FacilityType.objects.get(title=f["type"])
    except models.FacilityType.DoesNotExist:
      type = models.FacilityType()
      type.title = f["type"]
      type.save()
      facility.type = type

  if f["district"]:
    try:
      facility.district = models.District.objects.get(title=f["district"])
    except models.District.DoesNotExist:
      district = models.District()
      district.title = f["district"]
      district.save()
      facility.district = district
  facility.save()
  print "added ", facility



def main():
  with transaction.commit_on_success():
    for line in fileinput.input():
      f = json.loads(line)
      import_facility(f)



if __name__ == '__main__':
  main()


