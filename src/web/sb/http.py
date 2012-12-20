import json
import datetime
import time

from django import http


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

def to_json_response(data, status=200):
  """Convert 'data' to a JSON response.

  This serializes 'data' to JSON and returns an HTTP response with the
  "Content-Type" header set to "application/json".

  Arguments:
  data --- any, a value that json.dumps can marshal

  Returns
  django.http.HttpResponse
  """
  return http.HttpResponse(json.dumps(data, default=_to_json_default),
                      status=status,
                      content_type="application/json")
