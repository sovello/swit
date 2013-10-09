from django.core.management.base import BaseCommand, CommandError
from sb.healthworker.models import HealthWorker

class Command(BaseCommand):
  args = ''
  help = 'HealthWorker.auto_verify'

  def handle(self, *args, **options):
    statuses = [
        "Unverified",
        "Verified By Payroll #",
        "Verified By Reg #",
        "Manually Verified",
        "Verified By Phone #",
        "Verified By Name"
      ]

    for hw in HealthWorker.objects.filter(verification_state=HealthWorker.UNVERIFIED).order_by('id').all():
      hw.auto_verify()
      if hw.verification_state != HealthWorker.UNVERIFIED:
        status = statuses[hw.verification_state]
        if hw.verification_state == HealthWorker.NAME_VERIFIED:
          status += " (matched '%s')" % hw.get_matching_name()
        print "'%s' (id #%d): %s" % (hw.name, hw.id, status)

    print "Summary:"
    for i in range(len(statuses)):
      print "%s: %d" % (statuses[i], HealthWorker.objects.filter(verification_state__exact=i).count())

