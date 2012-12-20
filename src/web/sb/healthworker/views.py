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



