import contextlib
import datetime
import optparse
import re
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.db import transaction
from django.utils.timezone import utc
import tablib

from sb.healthworker import models

class Command(BaseCommand):
  help = 'Sends a CUG request email'

  def fix_phone(self, phone):
    if phone.startswith('+2557'):
      return '07' + phone[5:]
    elif phone.startswith('7'):
      return '0' + phone

  def add_arguments(self, parser):
    parser.add_argument('--save', action='store_true', help=u'save changes')
    parser.add_argument('--src-email', default="hostmaster@switchboard.org")
    parser.add_argument('--dst-email', default="brandon@switchboard.org")
    parser.add_argument('--cc-email', default=[], action='append')

  def handle(self, *args, **options):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    with transaction.atomic():
      health_workers = models.HealthWorker.objects
      health_workers = health_workers.filter(is_closed_user_group=False)
      health_workers = health_workers.exclude(verification_state=None)
      health_workers = health_workers.exclude(verification_state=models.HealthWorker.UNVERIFIED)
      health_workers = health_workers.exclude(vodacom_phone=None)
      health_workers = health_workers.exclude(vodacom_phone=u'')
      health_workers = health_workers.all()
      health_workers = list(health_workers)
      for h in health_workers:
        if not h.request_closed_user_group_at:
          h.request_closed_user_group_at = now
          h.save()

    # Compose xls and send it
    data = [(self.fix_phone(i.vodacom_phone), i.surname or u"") for i in health_workers]
    dataset = tablib.Dataset(*data, headers=("phone", "name"))
    email = EmailMessage(u"Closed User Group Request %s" % (now, ),
                         u"Please add the attached users to the closed user group.  Thanks!",
                         options['src_email'],
                         [ options['dst_email'] ],
                         cc=options['cc_email'] if options['cc_email'] else None)
    filename = now.strftime("cug-request-%Y%m%d-%H%M%S.xls")    
    email.attach(filename, dataset.xls, "application/vnd.ms-excel")
    email.send()
