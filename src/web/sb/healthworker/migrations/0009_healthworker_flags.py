# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
      db.add_column('healthworker_healthworker', 'is_vodacom_user_group', models.NullBooleanField())
      db.add_column('healthworker_healthworker', 'is_valid_healthworker', models.NullBooleanField())

    def backwards(self, orm):
      pass

