import datetime
import fileinput
import json
import re
import sys

from django.db import transaction

from sb.healthworker import models
from sb.healthworker.datasets import _helpers

def _first(x):
  for i in x:
    return i

# swahili months
_months = {
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

def _parse_birth_date(s):
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
    month = _months[d["month1"].lower()]
    year = int(d["year1"])
    if year < 100:
      year += 1900
  # Try a bunch of date combinations
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

def import_new_payroll(item):
  pr = _first(models.MCTPayroll.objects.filter(check_number=item["check_number"]).all())
  if pr is None:
    pr = models.MCTPayroll()
  pr.last_name = item["last_name"]
  pr.name = item["full_name"]
  pr.designation = item["designation"]
  if item["designation"]:
    pr.specialty = _first(models.Specialty.objects.filter(title__iexact=item["designation"]).all())
  if item["district"]:
    pr.facility = _first(models.Facility.objects.filter(title__iexact=item["district"]).all())
    pr.region = _first(models.Region.objects.filter(title__iexact=item["district"]).all())
  pr.birthdate = _parse_birth_date(item["date_of_birth"])
  pr.check_number = item["check_number"]
  pr.district = item["district"]
  pr.save()

def run():
  with transaction.commit_on_success():
    items = _helpers.read_csv(_helpers.get_path('payroll_payroll 1 Mar 2013.csv'),
                              fields=["id", "full_name", "last_name",
                                      "check_number", "date_of_birth",
                                      "designation", "district"])
    for item in items:
      import_new_payroll(item)

    for hw in models.HealthWorker.objects.all():
      hw.auto_verify()

if __name__ == '__main__':
  run()

