# Copyright 2012 Switchboard, Inc


import datetime
import json
import time

from django.core import serializers
from django.http import HttpResponse

from sb.healthworker import models

def _to_json_default(an_object):
  "JSON converter function to convert dates and datetimes to UTC timestamps"
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
  """Convert 'data' to a JSON response.

  This serializes 'data' to JSON and returns an HTTP response with the
  "Content-Type" header set to "application/json".

  Arguments:
  data --- any, a value that json.dumps can marshal

  Returns
  django.http.HttpResponse
  """
  return HttpResponse(json.dumps(data, default=_to_json_default),
                      status=status,
                      content_type="application/json")

def _cadre_to_dictionary(cadre):
  "Convert a Cadre to a dictionary suitable for JSON encoding"
  return {"created_at": cadre.created_at,
          "updated_at": cadre.updated_at,
          "id": cadre.id,
          "title": cadre.title}

def on_cadre_index(request):
  """Get a list of cadres"""
  cadres = models.Cadre.objects.all()
  return _to_json_response(map(_cadre_to_dictionary, cadres))


