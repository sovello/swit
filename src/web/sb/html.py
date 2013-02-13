import os.path

import django.http
import mako
import mako.lookup

_name_to_template = {}

def render_template(package, path, **context):
  key = package, path
  package_parts = package.split('.')
  mod = __import__(package)
  for p in package.split('.')[1:]:
    mod = getattr(mod, p)
  mod_dir = os.path.split(mod.__file__)[0]
  tmpl_dir = os.path.join(mod_dir, 'templates')
  lookup = mako.lookup.TemplateLookup(directories=[tmpl_dir])
  template = lookup.get_template(path)
  buf = template.render(**context)
  return buf

def render_response(request, package, path, **context):
  context.update({"request": request})
  buf = render_template(package, path, **context)
  return django.http.HttpResponse(buf)

