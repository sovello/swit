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

def _cadre_to_dictionary(cadre):
  "Convert a Cadre to a dictionary suitable for JSON encoding"
  return {"created_at": cadre.created_at,
          "updated_at": cadre.updated_at,
          "id": cadre.id,
          "abbreviation": cadre.abbreviation,
          "title": cadre.title}

def on_cadre_index(request):
  """Get a list of cadres"""
  cadres = models.Cadre.objects.all()
  return http.to_json_response(
      {"status": OK,
       "cadres": map(_cadre_to_dictionary, cadres)})

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
  regions = models.Region.objects.all()
  response = {
      "status": OK,
      "regions": map(_region_to_dictionary, regions)}
  return http.to_json_response(response)

def _facility_to_dictionary(facility):
  return {
      "id": facility.id,
      "title": facility.title,
      "region_id": facility.region_id,
      "created_at": facility.created_at,
      "updated_at": facility.updated_at}

def on_facility_index(request):
  facilities = models.Facility.objects.all()
  response = {
      "status": OK,
      "facilities": map(_facility_to_dictionary, facilities)}
  return http.to_json_response(response)

