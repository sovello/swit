import datetime
import re

from django.db import transaction

from sb.healthworker.datasets import _helpers
from sb.healthworker.models import MCTRegistration, Specialty

def remove_unlinked_registration_entries():
  MCTRegistration.objects.filter(health_worker__isnull=True).delete()

def import_new_entry(item):
  worker = MCTRegistration()
  worker.registration_type, worker.registration_number = parse_registration_number(item["Registration No"])
  worker.address = item["Address"]
  worker.birthdate = parse_dob(item["DOB"])
  worker.save()
  cadre = None
  if item["Cadre"]:
    for cadre in Specialty.objects.filter(abbreviation=item["Cadre"]).all():
      worker.specialties.add(cadre)
  worker.country = "TZ" if item["Nationality"] == "Tanzanian" else None
  worker.cadre = item["Cadre"]
  worker.category = item["Category"]
  worker.current_employer = item["Current Employer"]
  worker.dates_of_registration_full = item["Full"]
  worker.dates_of_registration_provisional = item["Provisional"]
  worker.dates_of_registration_temporary = item["Temporary"]
  worker.employer_during_internship = item["Employer during internship"]
  worker.file_number = item["MCT File No"]
  worker.name = item["Name"]
  worker.qualification_final = item["Final"]
  worker.qualification_provisional = item["Provisional"]
  worker.qualification_specialization_1 = item["Specialization 1"]
  worker.qualification_specialization_2 = item["Specialization 2"]
  worker.specialty = item["Specialty"]
  if cadre and item["Specialty"]:
    specialties = Specialty.objects.filter(title__iexact=item["Specialty"])
    for s in specialties:
      if s.is_child_of(cadre):
        worker.specialties.add(s)
        worker.specialty_duration = item["DUR"]
        worker.save()
  worker.save()

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

reg_prec = {"f": 0, "i": 1, "p": 2}

def parse_registration_number(reg_number):
  registration_numbers = filter(bool, reg_number.split(","))
  if registration_numbers:
    registration_numbers.sort(key=lambda i: reg_prec.get(i[0].lower(), 100))
    return registration_numbers[0][0], registration_numbers[0][1:]
  else:
    return None, None

def run():
  path = _helpers.get_path('mct-20130307-individual.csv')
  mct_rows = _helpers.read_csv(path)
  with transaction.commit_on_success():
    remove_unlinked_registration_entries()
    for mct_row in mct_rows:
      import_new_entry(mct_row)

if __name__ == '__main__':
  run()


