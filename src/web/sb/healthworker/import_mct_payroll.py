import datetime
import json
import fileinput
import re

from sb.healthworker import models
from django.db import transaction

def first(x):
  for i in x:
    return i

months = {
  "jan": 1,
  "feb": 2,
  "mac": 3,
  "apr": 4,
  "mei": 5,
  "jun": 6,
  "jul": 7,
  "ago": 8,
  "sep": 9,
  "okt": 10,
  "nov": 11,
  "dec": 12,
  "des": 12}

def parse_birth_date(s):
  s = s.strip()
  if not s:
    return None
  match = re.match(r"""^
    (?P<month0>\d+)/(?P<day0>\d+)/(?P<year0>\d+)
    |(?P<day1>\d+)-(?P<month1>\w+)-(?P<year1>\d+)
    $""", s, re.M | re.X)
  if not match:
    return None
  d = match.groupdict()
  if d['year0']:
    year = int(d["year0"])
    day = int(d["day0"])
    month = int(d["month0"])
  else:
    day = int(d["day1"])
    month = months[d["month1"].lower()]
    year = int(d["year1"])
    if year < 100:
      year += 1900
  try:
    return datetime.date(year, month, day)
  except ValueError:
    try:
      return datetime.date(day, month, year)
    except ValueError:
      try:
        return datetime.date(year, day, month)
      except ValueError:
        pass

def main():
  with transaction.commit_on_success():
    for idx, line in enumerate(fileinput.input()):
      vals = line.decode("utf-8").rstrip("\n").split("\t")
      if idx == 0:
        fields = vals
        continue
      item = dict(zip(fields, vals))

      pr = models.MCTPayroll()
      pr.last_name = item["last_name"]
      pr.name = item["full_name"]
      pr.designation = item["designation"]
      if item["designation"]:
        pr.specialty = first(models.Specialty.objects.filter(title__iexact=item["designation"]).all())
      if item["district"]:
        pr.facility = first(models.Facility.objects.filter(title__iexact=item["district"]).all())
        pr.region = first(models.Region.objects.filter(title__iexact=item["district"]).all())
      pr.birthdate = parse_birth_date(item["date_of_birth"])
      pr.check_number = item["check_number"]
      pr.district = item["district"]
      pr.save()

if __name__ == "__main__":
  main()



