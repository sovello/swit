#!/usr/bin/python
import sys

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

def try_create_user(username, email, password):
  try:
     auth_models.User.objects.get(username=username)
  except auth_models.User.DoesNotExist:
     print "Creating", username
     auth_models.User.objects.create_superuser(username, email, password)

if __name__ == "__main__":
  try_create_user(sys.argv[1], sys.argv[2], sys.argv[3])

