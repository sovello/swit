"Utility functions"""

import urllib2
import base64
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

def send_vumigo_sms(to_addr, content):
  if settings.VUMIGO_API_URL is None:
    raise ValueError("Can't send SMS, VUMIGO_API_URL not configured")
  username = settings.VUMIGO_CONVERSATION_ID
  pasword = settings.VUMIGO_CONVERSATION_TOKEN
  request = urllib2.Request(settings.VUMIGO_API_URL)
  basic_auth = base64.standard_b64encode('%s:%s' % (username, password))
  request.add_header("Authorization", "Basic %s" % basic_auth)
  request.add_header("Content-Type", "application/json")
  request.add_data(json.dumps({
    "content": content,
    "to_addr": to_addr
  }))
  urllib2.urlopen(request)
