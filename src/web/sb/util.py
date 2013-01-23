"Utility functions"""

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

