import csv
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from sb.healthworker.models import HealthWorker, RegistrationStatus, RegistrationAnswer

class Command(BaseCommand):

  args = ''
  help = ''

  option_list = BaseCommand.option_list + (make_option('-i', '--include-states',
      action='append',
      type="int",
      help='Include users that dropped off on the given state(s)'
    ), make_option('-x', '--exclude-states',
      action='append',
      type="int",
      help='Exclude users that dropped off on the given state(s)'
    ), make_option('-f', '--filename',
      action='store',
      type="string",
      default="dropoffs.csv",
      help='Export filename'
    ))

  def handle(self, *args, **options):
    # Get list of states we want to process
    states = options['include_states'] if options['include_states'] else range(RegistrationStatus.NUM_STATES)
    if options['exclude_states']:
      for x in options['exclude_states']:
        try:
          states.remove(x)
        except ValueError:
          pass

    # Write CSV file
    with open(options['filename'], 'wb') as csvfile:
      writer = csv.writer(csvfile)
      users = RegistrationStatus.objects.filter(last_state__in=states, registered=False)
      for user in users:
        # Get user's language
        lang = ''
        answers = RegistrationAnswer.objects.filter(msisdn=user.msisdn, question=RegistrationStatus.INTRO)[:1]
        if answers:
          lang = answers[0].answer

        # Write user to csv
        writer.writerow([user.msisdn, lang])

