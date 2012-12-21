"Importer for the Tanzanian Minsistry of Health (MCT?) Registration Database Spreadsheet"
import datetime
import fileinput
import re

from sb.healthworker import models
from django.db import transaction


def parse_dob(s):
  """Parse the date of birth column

  This appears to be of the form MM/DD/YY
  """
  match = re.match(r"(?P<month>\d+)[/](?P<day>\d+)[/](?P<year>\d+)", s)
  if match:
    d = match.groupdict()
    try:
      return datetime.date(int(d["year"]), int(d["month"]), int(d["day"]))
    except ValueError:
      pass

def main():
  """main loop"""
  keys = None
  with transaction.commit_on_success():
    for idx, a_line in enumerate(fileinput.input()):
      if idx == 0:
        continue
      fields = a_line.rstrip('\n').split("\t")
      if not fields:
        continue
      if not a_line:
        continue
      if idx == 1:
        keys = fields
        continue
      item = dict(zip(keys, fields))
      registration_numbers = filter(bool, item["Registration No"].split(","))
      worker = models.HealthWorker()
      # get auto increment ID
      worker.save()
      for registration_number in registration_numbers:
        if not registration_number:
          continue
        num = models.MCTRegistrationNumber()
        num.number = registration_number
        num.health_worker = worker
        num.save()
      worker.address = item["Address"]
      worker.birthdate = parse_dob(item["DOB"])
      cadre = models.Specialty.get_or_create_by_abbreviation(item["Cadre"])
      if cadre is not None:
        worker.specialties.add(cadre)
      worker.country = "TZ" if item["Nationality"] == "Tanzanian" else None
      worker.mct_category = item["Category"]
      worker.mct_current_employer = item["Current Employer"]
      worker.mct_dates_of_registration_full = item["Full"]
      worker.mct_dates_of_registration_provisional = item["Provisional"]
      worker.mct_dates_of_registration_temporary = item["Temporary"]
      worker.mct_employer_during_internship = item["Employer during internship"]
      worker.mct_file_number = item["MCT File No"]
      worker.mct_qualification_final = item["Final"]
      worker.mct_qualification_provisional = item["Provisional"]
      worker.mct_qualification_specialization_1 = item["Specialization 1"]
      worker.mct_qualification_specialization_2 = item["Specialization 2"]
      worker.mct_specialty = item["Specialty"]
      if cadre and item["Specialty"]:
        specialties = models.Specialty.objects.filter(title__iexact=item["Specialty"])
        for s in specialties:
          if s.is_child_of(cadre):
            worker.specialties.add(s)
      worker.mct_specialty_duration = item["DUR"]
      worker.name = item["Name"]
      worker.save()

def get_cadre_by_abbreviation(abbrev):
  """Get or create a cadre by abbrevation"""
  if not abbrev:
    return
  try:
    return models.Specialty.objects.get(abbreviation=abbrev)
  except models.Specialty.DoesNotExist:
    cadre = models.Specialty()
    cadre.abbreviation = abbrev
    cadre.title = abbrev
    cadre.save()
    return cadre

if __name__ == "__main__":
  main()


