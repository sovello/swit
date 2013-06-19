from django.db import transaction
from south.db import db
from south.v2 import SchemaMigration

from sb.healthworker import models

def run():
  models.Region.get_or_create_region_by_title_type('TZ', 'Country')


