import contextlib
import datetime
import optparse
import re

from sb.healthworker import models
from django.db import transaction
from django.core.mail import EmailMessage


def csv_escape(s):
  if not s:
    s = u''
  s = u'"%s"' % (s, )
  return s

def to_csv(vals):
  return u','.join(map(csv_escape, vals))

def healthworkers_to_csv(health_workers):
  buf = []
  buf.append(to_csv(['name', 'phone']))
  for h in health_workers:
    buf.append(to_csv([h.name, h.vodacom_phone]))
  return u'\n'.join(buf).encode('utf-8')

def main():
  parser = optparse.OptionParser()
  parser.add_option('--save', action='store_true', help=u'save changes')
  parser.add_option('--src-email', default="hostmaster@switchboard.org")
  parser.add_option('--dst-email', default="bickfordb@gmail.com")

  opts, args = parser.parse_args()

  cols = ['name', 'phone']
  model_cols = ['name', 'vodacom_phone']

  @contextlib.contextmanager
  def commit_block():
    with transaction.commit_manually():
      if opts.save:
        try:
          yield
          transaction.commit()
        except:
          transaction.rollback()
          raise
      else:
        try:
          yield
          transaction.rollback()
        except:
          transaction.rollback()
          raise


  with commit_block():
    health_workers = models.HealthWorker.objects
    health_workers = health_workers.filter(request_closed_user_group_at=None)
    health_workers = health_workers.filter(is_closed_user_group=False)
    health_workers = health_workers.exclude(verification_state=None)
    health_workers = health_workers.exclude(verification_state=models.HealthWorker.UNVERIFIED)
    health_workers = health_workers.exclude(vodacom_phone=None)
    health_workers = health_workers.exclude(vodacom_phone=u'')
    health_workers = health_workers.all()
    health_workers = list(health_workers)
    for h in health_workers:
      if not h.request_closed_user_group_at:
          h.request_closed_user_group_at = datetime.datetime.now()
          h.save()
    if health_workers:
      csv = healthworkers_to_csv(health_workers)
      email = EmailMessage(u"Closed User Group Request %s" % (datetime.datetime.now(), ),
                           u"Please add the attached users to the closed user group.  Thanks!",
                           opts.src_email,
                           [opts.dst_email])
      filename = datetime.datetime.now().strftime("cug-request-%Y%m%d-%H%M%S.csv")
      email.attach(filename, csv, "text/csv")
      email.send()

if __name__ == "__main__":
  main()



