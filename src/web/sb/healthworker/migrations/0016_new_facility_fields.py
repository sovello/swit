import os.path
import re

from django.db import transaction
from south.v2 import SchemaMigration
from south.db import db

from django.db import models

class Migration(SchemaMigration):
    def forwards(self, orm):
      with transaction.commit_on_success():
        db.add_column('healthworker_facility', 'latitude', models.FloatField(null=True, blank=True))
        db.add_column('healthworker_facility', 'longitude', models.FloatField(null=True, blank=True))
        db.add_column('healthworker_facility', 'alternative_names', models.CharField(max_length=255, null=True, blank=True))
        db.add_column('healthworker_facility', 'status', models.CharField(max_length=255, null=True, blank=True))
        db.add_column('healthworker_facility', 'hmis', models.CharField(max_length=255, null=True, blank=True))
        db.add_column('healthworker_facility', 'remarks', models.CharField(max_length=255, null=True, blank=True))
        db.add_column('healthworker_facility', 'registration_num', models.CharField(max_length=255, null=True, blank=True))
        db.add_column('healthworker_facility', 'source', models.CharField(max_length=255, null=True, blank=True))

    def backwards(self, orm):
      pass

