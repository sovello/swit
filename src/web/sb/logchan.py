import datetime
import errno
import json
import os
import os.path
import re
import time

SB_CHANNEL_ROOT = "SB_CHANNEL_ROOT"

channel_root = os.environ.get(SB_CHANNEL_ROOT, "")

channel_pat = re.compile('^[a-zA-Z0-9-_]+$')

def write(channel_name, **args):
  ts = time.time()
  if not channel_pat.match(channel_name):
    raise ValueError("unexpected channel name")
  today = datetime.date.today()
  chan_dir = os.path.join(channel_root, channel_name)
  try:
    os.makedirs(chan_dir)
  except OSError, err:
    if err.errno != errno.EEXIST:
      raise

  path = today.strftime(channel_name + '-%Y%m%d.json')
  path = os.path.join(chan_dir, path)
  data = {
    "time": time.time(),
    "channel": channel_name,
    "data": args}
  buf = json.dumps(data)
  with open(path, "a") as a_file:
    a_file.write(buf + "\n")
