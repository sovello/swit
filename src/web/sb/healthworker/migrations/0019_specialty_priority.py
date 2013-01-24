import os.path
import re

from django.db import transaction
from south.v2 import SchemaMigration
from south.db import db

from django.db import models

class Migration(SchemaMigration):
    def forwards(self, orm):
      db.add_column('healthworker_specialty', 'priority', models.IntegerField(default=0, null=False, blank=True))

    def backwards(self, orm):
      pass

