from django.db import transaction
from south.db import db
from south.v2 import SchemaMigration

from sb.healthworker import models

class Migration(SchemaMigration):

    def forwards(self, orm):
      with transaction.commit_on_success():
        models.Region.get_or_create_region_by_title_type('TZ', 'Country')

    def backwards(self, orm):
      pass


