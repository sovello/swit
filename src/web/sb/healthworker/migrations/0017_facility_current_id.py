import os.path
import re

from django.db import transaction
from south.v2 import SchemaMigration
from south.db import db

from django.db import models

class Migration(SchemaMigration):
    def forwards(self, orm):
      with transaction.commit_on_success():
        db.add_column('healthworker_facility', 'current_id', models.CharField(max_length=255, null=True, blank=True))

    def backwards(self, orm):
      pass

