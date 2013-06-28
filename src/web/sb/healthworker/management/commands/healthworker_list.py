import csv
import datetime
import sys

from django.core.management.base import BaseCommand, CommandError

from sb.healthworker import models


class Command(BaseCommand):
  args = ''
  help = 'print a list of health workers'

  def handle(self, *args, **options):
    def fmt_date(x):
      if isinstance(x, datetime.datetime):
        return x.strftime('%Y-%m-%d %H:%M:%S')
      elif isinstance(x, datetime.date):
        return x.strftime('%Y-%m-%d')
      else:
        return u''

    items = []
    for hw in models.HealthWorker.objects.all():
      item = {}
      item['id'] = hw.id
      item['name'] = hw.name
      item['specialties'] = u', '.join([s.title for s in hw.specialties.all()])
      item['facility'] = hw.facility.title if hw.facility else u''
      item['birthdate'] = fmt_date(hw.birthdate)
      item['address'] = hw.address
      item['vodacom_phone'] = hw.vodacom_phone
      item['is_closed_user_group'] = hw.is_closed_user_group
      item['gender'] = hw.gender
      item['email'] = hw.email
      item['verification_state'] = hw.verification_state
      item['created_at'] = fmt_date(hw.created_at)
      items.append(item)
    w = csv.DictWriter(sys.stdout, items[0].keys())
    w.writeheader()
    w.writerows(items)







