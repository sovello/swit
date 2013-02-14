"Utility functions"""

import urllib2
import base64
import json
from django.conf import settings

def safe(f, *pos, **kw):
  """Try to execute f and return None if it fails"""
  try:
    return f(*pos, **kw)
  except:
    pass

def read_tsv(path):
  fields = []
  for idx, line in enumerate(open(path, 'r')):
    line = line.decode('utf-8').rstrip('\r\n')
    vals = line.split('\t')
    if idx == 0:
      fields = vals
      fields = [f.lower() for f in fields]
    else:
      item = dict(zip(fields, vals))
      yield item


class SmsSendingError(Exception):
  """Raised when SMS sending fails."""


def send_vumigo_sms(to_addr, content):
  if not settings.VUMIGO_SEND_SMSES:
    return
  if settings.VUMIGO_API_URL is None:
    raise ValueError("Can't send SMS, VUMIGO_API_URL not configured")
  username = settings.VUMIGO_ACCOUNT_ID
  password = settings.VUMIGO_CONVERSATION_TOKEN
  url = "%s/%s/messages.json" % (settings.VUMIGO_API_URL,
                                 settings.VUMIGO_CONVERSATION_ID)
  request = urllib2.Request(url)
  basic_auth = base64.standard_b64encode('%s:%s' % (username, password))
  request.add_header("Authorization", "Basic %s" % basic_auth)
  request.add_header("Content-Type", "application/json")
  request.add_data(json.dumps({
    "content": content,
    "to_addr": to_addr
  }))
  # urllib2 doesn't have a better way to do PUT :(
  request.get_method = lambda: "PUT"
  result = urllib2.urlopen(request)
  code = result.getcode()
  data = result.read()
  if code != 200:
    raise SmsSendingError("Failed to send SMS, response code: %d,"
                          " data: %r" % (code, data))
  return json.loads(data)
