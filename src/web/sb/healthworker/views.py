# Copyright 2012 Switchboard, Inc


import datetime
import json
import re
import time
import types

from django.core import serializers
from django.http import HttpResponse
from django import forms
from django.db import transaction

from sb import http
from sb.healthworker import models
import sb.util

OK = 0
ERROR_INVALID_INPUT = -1
ERROR_INVALID_PATTERN = -2

def _specialty_to_dictionary(specialty):
  "Convert a Specialty to a dictionary suitable for JSON encoding"
  return {"created_at": specialty.created_at,
          "updated_at": specialty.updated_at,
          "id": specialty.id,
          "parent_specialty_id": specialty.parent_specialty_id,
          "abbreviation": specialty.abbreviation,
          "title": specialty.title}

def on_specialty_index(request):
  """Get a list of specialties"""
  specialties = models.Specialty.objects.all()
  specialties = [i for i in specialties if not i.is_user_submitted]
  return http.to_json_response({
    "status": OK,
    "specialties": map(_specialty_to_dictionary, specialties)})

def on_mct_payroll_index(request):
  """Get a list of ministry of tanzania payroll entries"""
  mct_payroll_entries = models.MCTPayroll.objects
  check = sb.util.safe(lambda: request.GET["check"])
  offset = sb.util.safe(lambda: int(request.GET["offset"])) or 0
  count = sb.util.safe(lambda: int(request.GET["count"])) or 100
  if check:
    mct_payroll_entries = mct_payroll_entries.filter(check_number=check)
  mct_payroll_entries = mct_payroll_entries.all()
  mct_payroll_entries = list(mct_payroll_entries)
  total = len(mct_payroll_entries)
  mct_payroll_entries = mct_payroll_entries[offset:count]
  return http.to_json_response({
    "status": OK,
    "total": total,
    "mct_payrolls": [{
        "id": i.id,
        "name": i.name,
        "birthdate": i.birthdate,
        "designation": i.designation,
        "district": i.district,
        "specialty_id": i.specialty_id,
        "last_name": i.last_name,
        "region_id": i.region_id,
        "health_worker_id": i.health_worker_id,
        "facility_id": i.facility_id,
        "check_number": i.check_number}
      for i in mct_payroll_entries]})

def on_mct_registration_index(request):
  "Get information about a health worker"
  health_workers = models.MCTRegistration.objects
  num = request.GET.get("registration")
  name = request.GET.get("name")
  count = sb.util.safe(lambda:int(request.GET["count"])) or 100
  offset = sb.util.safe(lambda:int(request.GET["offset"])) or 0
  if num:
    health_workers = health_workers.filter(registration_number=num)
  if name:
    # FIXME: do levenshtein
    health_workers = health_workers.filter(name__istartswith=name)

  health_workers = list(health_workers.all())
  total = len(health_workers)

  health_worker_dicts = []
  for h in health_workers[offset:count]:
    health_worker_dicts.append({
      "address": h.address,
      "birthdate": h.birthdate,
      "cadre": h.cadre,
      "category": h.category,
      "country": h.country,
      "created_at": h.created_at,
      "current_employer": h.current_employer,
      "dates_of_registration_full": h.dates_of_registration_full,
      "dates_of_registration_provisional": h.dates_of_registration_provisional,
      "dates_of_registration_temporary": h.dates_of_registration_temporary,
      "email": h.email,
      "employer_during_internship": h.employer_during_internship,
      "facility": h.facility.id if h.facility else None,
      "file_number": h.file_number,
      "id": h.id,
      "name": h.name,
      "qualification_final": h.qualification_final,
      "qualification_provisional": h.qualification_provisional,
      "qualification_specialization_1": h.qualification_specialization_1,
      "qualification_specialization_2": h.qualification_specialization_2,
      "registration_number": h.registration_number,
      "registration_type": h.registration_type,
      "specialties": [i.id for i in h.specialties.all()],
      "specialty": h.specialty,
      "specialty_duration": h.specialty_duration,
      "updated_at": h.updated_at})
  response = {
      "status": OK,
      "total": total,
      "health_workers": health_worker_dicts}
  return http.to_json_response(response)

def _region_to_dictionary(region):
  if region is None:
    return None
  else:
    return {
        "title": region.title,
        "type": region.type.title if region.type is not None else None,
        "id": region.id,
        "parent_region_id": region.parent_region_id,
        "created_at": region.created_at,
        "updated_at": region.updated_at}

def on_region_index(request):
  regions = models.Region.objects
  for (query_param, key) in [
      ("parent_region_id", "parent_region_id"),
      ("type", "type__title__iexact"),
      ("title", "title__istartswith")]:
    val = request.GET.get(query_param)
    if val:
      regions = regions.filter(**{key: val})
  regions = regions.prefetch_related("type").all()
  response = {
      "status": OK,
      "regions": map(_region_to_dictionary, regions)}
  return http.to_json_response(response)

def _facility_to_dictionary(facility):
  return {
      "id": facility.id,
      "title": facility.title,
      "address": facility.address,
      "type": facility.type.title if facility.type else None,
      "place_type": facility.place_type,
      "serial_number": facility.serial_number,
      "owner": facility.owner,
      "ownership_type": facility.ownership_type,
      "phone": facility.phone,
      "place_type": facility.place_type,
      "region_id": facility.region_id,
      "created_at": facility.created_at,
      "updated_at": facility.updated_at}

def on_facility_index(request):
  facilities = models.Facility.objects
  title = request.GET.get("title")
  if title:
    facilities = facilities.filter(title__istartswith=title)
  region_id = request.GET.get("region")
  if region_id:
    # compute subregions here.
    region_ids = set()
    try:
      region = models.Region.objects.get(id=region_id)
    except models.Region.DoesNotExist:
      pass
    else:
      region_ids.add(region.id)
      region_ids.update(region.subregion_ids())
    facilities = facilities.filter(region_id__in=region_ids)
  facility_type = sb.util.safe(lambda:int(request.GET["type"]))
  if facility_type:
    facilities = facilities.filter(type_id=facility_type)

  facilities = facilities.prefetch_related("type")
  facilities = facilities.all()
  facilities = filter(lambda f: not f.is_user_submitted, facilities)
  response = {
      "status": OK,
      "facilities": map(_facility_to_dictionary, facilities)}
  return http.to_json_response(response)

_address_pat = re.compile(u"^.{1,255}$")
_email_pat = re.compile(u"^.+@.+$")
_name_pat = re.compile(u"^.{1,255}$")

def string_parser(pattern=None, required=False, min_length=None, max_length=None, strip=True):
  def parser(value):
    if value is None:
      if required:
        return None, ERROR_INVALID_INPUT
      else:
        return value, None
    if not isinstance(value, unicode):
      return None, ERROR_INVALID_INPUT
    if strip:
      value = value.strip()
    if pattern is not None:
      pat = re.compile(pattern) if isinstance(pattern, types.StringTypes) else pattern
      if not pat.match(value):
        return None, ERROR_INVALID_INPUT
    if min_length is not None and len(value) < min_length:
      return None, ERROR_INVALID_INPUT
    if max_length is not None and len(value) > max_length:
      return None, ERROR_INVALID_INPUT
    return value, None
  return parser

def dictionary_parser(key_to_parser):
  def parser(data):
    if not data:
      return None, {"status": ERROR_INVALID_INPUT, "key": None}
    if not isinstance(data, dict):
      return None, {"status": ERROR_INVALID_INPUT, "key": None}
    result = {}
    for key, parser in key_to_parser.items():
      v = data.get(key)
      v, status = parser(v)
      if status:
        return None, {"key": key, "status": status}
      result[key] = v
    return result, None
  return parser

def list_parser(parser, required=None):
  def parser0(values):
    if not isinstance(values, (list, tuple, type(None))):
      return None, ERROR_INVALID_INPUT
    if not values:
      if not required:
        return [], None
      else:
        return None, ERROR_INVALID_INPUT
    result = []
    for v in values:
      parsed, status = parser(v)
      if status:
        return None, status
      else:
        result.append(parsed)
    return result, None
  return parser0

def foreign_key_parser(model_class, required=None):
  def parser(value):
    if value is None:
      if required:
        return None, ERROR_INVALID_INPUT
      else:
        return None, None
    try:
      return model_class.objects.get(id=value), None
    except model_class.DoesNotExist:
      return None, ERROR_INVALID_INPUT
  return parser

def date_parser(required=None):
  def parser(value):
    if not isinstance(value, (dict, type(None))):
      return None, ERROR_INVALID_INPUT
    if not value:
      if required:
        return None, ERROR_INVALID_INPUT
      else:
        return None, None
    result = sb.util.safe(lambda: datetime.date(value["year"], value["month"], value["day"]))
    return result, None
  return parser

def parse_healthworker_input(data):
  parser = dictionary_parser({
    "address": string_parser(pattern="^.{0,255}$", required=False),
    "birthdate": date_parser(required=False),
    "country": string_parser(min_length=2, max_length=3, required=False),
    "email": string_parser(pattern="^.+@.+$", required=False),
    "facility": foreign_key_parser(models.Facility, required=False),
    "language": string_parser(max_length=16, required=False),
    "name": string_parser(min_length=1, required=True),
    "specialties": list_parser(foreign_key_parser(models.Specialty, required=False)),
    "vodacom_phone": string_parser(required=False, max_length=255),
    "mct_payroll": foreign_key_parser(models.MCTPayroll, required=False),
    "mct_registration": foreign_key_parser(models.MCTRegistration, required=False),
    "other_phone": string_parser(required=False, max_length=255)})
  return parser(data)

def on_health_workers_save(request):
  if not request.is_json:
    return http.to_json_response({
      "status": ERROR_INVALID_INPUT,
      "message": "expecting JSON input"})
  data, error = parse_healthworker_input(request.JSON)
  if error:
    return http.to_json_response({"status": error["status"], "key": error.get("key")})

  with transaction.commit_on_success():
    health_worker = models.HealthWorker()
    health_worker.address = data["address"]
    health_worker.birthdate = data["birthdate"]
    health_worker.name = data["name"]
    health_worker.country = data["country"]
    health_worker.email = data["email"]
    health_worker.facility = data["facility"]
    for i in data["specialties"]:
      health_worker.save()
      health_worker.specialties.add(i)
    health_worker.other_phone = data["other_phone"]
    health_worker.vodacom_phone = data["vodacom_phone"]
    health_worker.language = data["language"]
    health_worker.save()
    if data["mct_registration"]:
      if data["mct_registration"].health_worker is None:
        data["mct_registration"].health_worker = health_worker
        data["mct_registration"].save()
    if data["mct_payroll"]:
      if data["mct_payroll"].health_worker is None:
        data["mct_payroll"].health_worker = health_worker
        data["mct_payroll"].save()
  return http.to_json_response({"status": OK})

def on_health_worker(request):
  if request.method == "POST":
    return on_health_workers_save(request)
  else:
    return http.not_found()

def on_facility_type_index(request):
  facility_types = [{"id": f.id,
                     "created_at": f.created_at,
                     "updated_at": f.updated_at,
                     "title": f.title}
                     for f in models.FacilityType.objects.all()]
  response = {"status": OK, "facility_types": facility_types}
  return http.to_json_response(response)

def on_specialty(request):
  if request.method != "POST":
    return on_specialty_index(request)
  else:
    return on_specialty_create(request)

def on_specialty_create(request):
  if not request.is_json:
    return http.to_json_response({
      "status": ERROR_INVALID_INPUT,
      "message": "expecting JSON input"})
  data, error = parse_specialty_input(request.JSON)
  if error:
    return http.to_json_response({"status": error["status"], "key": error.get("key")})

  with transaction.commit_on_success():
    if list(models.Specialty.objects.filter(title=data["title"], parent_specialty=data["parent_specialty"]).all()):
      return http.to_json_response({"status": ERROR_INVALID_INPUT})
    specialty = models.Specialty()
    specialty.title = data["title"]
    specialty.parent_specialty = data["parent_specialty"]
    specialty.msisdn = data["msisdn"]
    specialty.is_user_submitted = True
    specialty.save()
    return http.to_json_response({"status": OK, "id": specialty.id})

def parse_specialty_input(data):
  parser = dictionary_parser({
    "title": string_parser(pattern="^.{1,255}$", required=False),
    "msisdn": string_parser(pattern="^.{1,255}$", required=False),
    "parent_specialty": foreign_key_parser(models.Specialty, required=False)})
  return parser(data)

def on_facility(request):
  if request.method != "POST":
    return on_facility_index(request)
  else:
    return on_facility_create(request)

def parse_facility_input(data):
  parser = dictionary_parser({
    "title": string_parser(pattern="^.{1,255}$", required=True),
    "address": string_parser(pattern="^.{1,1000}$", required=False),
    "msisdn": string_parser(pattern="^.{1,255}$", required=False),
    "type": foreign_key_parser(models.FacilityType, required=False),
    "region": foreign_key_parser(models.Region, required=False)})
  return parser(data)

def on_facility_create(request):
  if not request.is_json:
    return http.to_json_response({
      "status": ERROR_INVALID_INPUT,
      "message": "expecting JSON input"})
  data, error = parse_facility_input(request.JSON)
  if error:
    return http.to_json_response({"status": error["status"], "key": error.get("key")})
  with transaction.commit_on_success():
    # skip adding facilities with exactly the same title, region
    if list(models.Facility.objects.filter(title=data["title"],
                                           address=data["address"],
                                           region=data["region"]).all()):
      return http.to_json_response({"status": ERROR_INVALID_INPUT})
    facility = models.Facility()
    facility.title = data["title"]
    facility.address = data["address"]
    facility.region = data["region"]
    facility.msisdn = data["msisdn"]
    facility.is_user_submitted = True
    facility.save()
    return http.to_json_response({"status": OK, "id": facility.id})

