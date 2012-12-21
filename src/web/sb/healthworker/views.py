# Copyright 2012 Switchboard, Inc


import datetime
import json
import time

from django.core import serializers
from django.http import HttpResponse

from sb import http
from sb.healthworker import models

OK = 0
ERROR_INVALID_INPUT = -1

def _specialty_to_dictionary(specialty):
  "Convert a Specialty to a dictionary suitable for JSON encoding"
  return {"created_at": specialty.created_at,
          "updated_at": specialty.updated_at,
          "id": specialty.id,
          "abbreviation": specialty.abbreviation,
          "title": specialty.title}

def on_specialty_index(request):
  """Get a list of specialties"""
  specialties = models.Specialty.objects.all()
  return http.to_json_response(
      {"status": OK,
       "specialties": map(_specialty_to_dictionary, specialties)})

def on_healthworker_index(request):
  "Get information about a health worker"
  response = {
      "status": ERROR_INVALID_INPUT,
      "health_worker": None}
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
  regions = regions.prefetch_related('type').all()
  response = {
      "status": OK,
      "regions": map(_region_to_dictionary, regions)}
  return http.to_json_response(response)

def _facility_to_dictionary(facility):
  return {
      "id": facility.id,
      "title": facility.title,
      "address": facility.address,
      "type": facility.type.title,
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
  region_id = request.GET.get("region_id")
  if region_id:
    # compute subregions here.
    facilities = facilities.filter(region_id=region_id)
  facilities = facilities.prefetch_related("type")
  facilities = facilities.all()
  response = {
      "status": OK,
      "facilities": map(_facility_to_dictionary, facilities)}
  return http.to_json_response(response)

