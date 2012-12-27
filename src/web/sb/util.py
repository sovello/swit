"Utility functions"""

def safe(f, *pos, **kw):
  """Try to execute f and return None if it fails"""
  try:
    return f(*pos, **kw)
  except:
    pass


