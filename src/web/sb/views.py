import json
from sb import http

def home(request):
  return http.to_json_response({"status": 0})

