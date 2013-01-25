import json
import datetime
import time

from django import http

import sb.util

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
  return http.HttpResponse(json.dumps(data, default=_to_json_default, indent=2),
                      status=status,
                      content_type="application/json")


def not_found():
  "Return a not-found response"
  return http.HttpResponse(status=404)

def add_json_data(request):
  content_type = request.META.get("CONTENT_TYPE", "")
  request.JSON = {}
  request.is_json = False
  if content_type.lower() == "application/json":
    request.JSON = sb.util.safe(lambda: json.loads(request.body))
    if request.JSON is None:
      request.JSON = {}
    else:
      request.is_json = True

class JSONMiddleware(object):
  def process_request(self, request):
    add_json_data(request)

  def process_view(self, request, view_func, view_args, view_kwargs):
    pass

  def process_response(self, request, response):
    return response

  def process_template_response(self, request, response):
    return response

  def process_exception(self, request, exception):
    pass



