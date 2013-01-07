# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        db.alter_column('healthworker_healthworker', 'gender',
            models.CharField(max_length=16, choices=[("male", "Male"), ("female", "Female")], null=True))

    def backwards(self, orm):
        db.alter_column('healthworker_healthworker', 'gender',
            models.CharField(max_length=16, choices=[("male", "Male"), ("female", "Female")], null=False))

