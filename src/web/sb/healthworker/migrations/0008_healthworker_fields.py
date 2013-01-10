# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
      db.add_column('healthworker_healthworker', 'language', models.CharField(max_length=32, blank=True, null=True))
      db.add_column('healthworker_facility', 'msisdn', models.CharField(max_length=32, blank=True, null=True))
      db.add_column('healthworker_facility', 'is_user_submitted', models.NullBooleanField())
      db.add_column('healthworker_specialty', 'msisdn', models.CharField(max_length=32, blank=True, null=True))
      db.add_column('healthworker_specialty', 'is_user_submitted', models.NullBooleanField())

    def backwards(self, orm):
      pass

