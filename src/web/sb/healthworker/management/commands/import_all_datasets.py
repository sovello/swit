from django.core.management.base import BaseCommand, CommandError
from sb.healthworker.dataset import import_all_datasets

class Command(BaseCommand):
  args = ''
  help = 'import datasets'

  def handle(self, *args, **options):
    import_all_datasets()


