# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
  def forwards(self, orm):
    db.add_column('healthworker_healthworker',
                  'mct_registration_num',
                  models.CharField(null=True, max_length=128, blank=True))
    db.add_column('healthworker_healthworker',
                  'surname',
                  models.CharField(null=True, max_length=128, blank=True))
    db.add_column('healthworker_healthworker',
                  'mct_payroll_num',
                  models.CharField(null=True, max_length=128, blank=True))

  def backwards(self, orm):
    db.drop_column('healthworker_healthworker', 'mct_payroll_num')
    db.drop_column('healthworker_healthworker', 'mct_registration_num')
    db.drop_column('healthworker_healthworker', 'surname')

