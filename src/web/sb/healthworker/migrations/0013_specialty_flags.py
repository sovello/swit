# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    def forwards(self, orm):
      db.add_column('healthworker_specialty', 'is_query_subspecialties', models.BooleanField(default=False, blank=True))

    def backwards(self, orm):
      pass

