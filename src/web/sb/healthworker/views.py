# Copyright 2012 Switchboard, Inc


import datetime
import json
import time

from django.core import serializers
from django.http import HttpResponse

from sb.healthworker import models

def _to_json_default(an_object):
  if an_object is None:
    return None
  elif isinstance(an_object, datetime.datetime):
    return time.mktime(an_object.utctimetuple())
  elif isinstance(an_object, datetime.date):
    return {"year": an_object.year,
            "month": an_object.month,
            "day": an_object.day}
  else:
    raise TypeError(type(an_object))

def _to_json_response(data, status=200):
  return HttpResponse(json.dumps(data, default=_to_json_default),
                      status=status,
                      content_type="application/json")

def _to_timestamp(a_date_time):
  "Convert a date time object to a timestamp"
  return time.mktime(a_date_time.utctimetuple()) if a_date_time else None

def _cadre_to_dictionary(cadre):
  "Convert a Cadre to a dictionary suitable for JSON encoding"
  return {"created_at": cadre.created_at,
          "updated_at": cadre.updated_at,
          "title": cadre.title}

def on_cadre_index(request):
  cadres = models.Cadre.objects.all()
  return _to_json_response(map(_cadre_to_dictionary, cadres))

