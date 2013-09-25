import datetime
import re

from django.db import transaction

from sb.healthworker.datasets import _helpers
from sb.healthworker.models import NGO, NGORegistration

def format_phone_number(phone_number):
  phone_number = re.sub('[\s\.-]', '', phone_number)
  if not phone_number.startswith('+'):
    phone_number = "+%s" % phone_number
  return phone_number

#First Name,Middle Name,Last Name,Cadre,District,Duty Station,Vodacom #,Other Tel #,Payroll #,MCT License #,E-mail,Town/City,Region,NGO
def import_new_entry(item, ngo, list_num):
  # Strip all values of leading and trailing whitespace
  for k,v in item.items():
    if item[k] is not None:
      item[k] = v.strip()

  worker = NGORegistration(ngo=ngo, list_num=list_num)

  # Ignore records with no name
  worker.name = ' '.join(filter(bool, [item["First Name"], item["Middle Name"], item["Last Name"]]))
  if not worker.name:
    return

  worker.cadre = item["Cadre"]
  worker.district = item["District"]
  worker.duty_station = item["Duty Station"]
  worker.phone_number = format_phone_number(item["Vodacom #"])
  worker.alt_phone_number = format_phone_number(item["Other Tel #"])
  worker.check_number = item["Payroll #"]
  worker.registration_number = item["MCT License #"]
  if worker.registration_number == 'Licensed': # bad data
    worker.registration_number = None
  worker.email = item["E-mail"]
  worker.city = item["Town/City"]
  worker.region = item["Region"]
  worker.save()

def import_ngo_list(filename, ngo_name, list_num, replace=True):
  path = _helpers.get_path(filename)
  rows = _helpers.read_csv(path)

  with transaction.commit_on_success():
    # Get/create NGO
    ngo = NGO.get_or_create_by_name(ngo_name)

    # Delete entries we already imported
    if replace:
      NGORegistration.objects.filter(ngo=ngo, list_num=list_num).delete()

    # Import csv contents
    for row in rows:
      import_new_entry(row, ngo, list_num)
