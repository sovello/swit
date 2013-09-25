import datetime
import re

from django.db import transaction

from sb.healthworker.datasets import _helpers
from sb.healthworker.models import DMORegistration

# Useful during testing
def remove_unlinked_registration_entries():
  DMORegistration.objects.filter(health_worker__isnull=True).delete()

def parse_registration_number(reg_number):
  reg_type = None
  if reg_number:
    if reg_number[-1].isalpha():
      reg_type = reg_number[-1]
      reg_number = reg_number[0:-1]
    reg_number = reg_number.lstrip('-0').rstrip('-')
  return reg_type, reg_number

def parse_phone_number(phone_number):
  if phone_number:
    return "+255%s" % (phone_number)

def import_new_entry(item):
  # Strip all values of leading and trailing whitespace
  for k,v in item.items():
    if item[k] is not None:
      item[k] = v.strip()

  worker = DMORegistration()

  # Ignore records with no name
  worker.name = ' '.join(filter(bool, [item["FirstName"], item["MiddleName"], item["LastName"]]))
  if not worker.name:
    return

  worker.phone_number = parse_phone_number(item["Vodacom"])
  worker.registration_type, worker.registration_number = parse_registration_number(item["RegNo"])
  worker.cadre = item["Cadre"]
  worker.check_number = item["CNO"]
  worker.email = item["Email"]
  worker.city = item["City"]
  worker.district = item["District"]
  worker.region = item["Region"]
  worker.nationality = item["Nationality"]
  worker.gender = item["Gender"]
  worker.duty_station = item["DutyStation"]
  worker.department = item["Dep"]
  worker.save()

def run():
  path = _helpers.get_path('dmo_list_11Feb13.csv')
  rows = _helpers.read_csv(path)
  with transaction.commit_on_success():
    remove_unlinked_registration_entries()
    for row in rows:
      import_new_entry(row)

if __name__ == '__main__':
  run()


