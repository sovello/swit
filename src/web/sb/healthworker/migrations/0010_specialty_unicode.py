# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.db import transaction

from sb.healthworker import models
from sb.testing import is_testing

class Migration(SchemaMigration):

  def forwards(self, orm):
    if is_testing():
      return
    with transaction.commit_on_success():
      for s in models.Specialty.objects.all():
        s = s.title.replace(u'\u200e', '')

  def backwards(self, orm):
    pass

