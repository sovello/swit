from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from sb.healthworker.models import HealthWorker, RegistrationStatus, RegistrationAnswer, Specialty, Facility

class Command(BaseCommand):
  args = ''
  help = 'Retroactively register anyone that agreed to terms of service by looking at Redis data'

  def handle(self, *args, **options):
    num_attempts = 0
    num_registrations = 0

    for user in RegistrationStatus.objects.filter(registered=False).all():
      vodacom_phone = '+' + user.msisdn
      try:
        HealthWorker.objects.get(vodacom_phone=vodacom_phone)
      except MultipleObjectsReturned:
        # Shouldn't ever happen, but...
        pass
      except ObjectDoesNotExist:
        print "Attempting to register %s" % vodacom_phone
        num_attempts += 1

        try:
          RegistrationAnswer.objects.get(msisdn=user.msisdn, question=RegistrationStatus.TERMS, answer='yes')
        except ObjectDoesNotExist:
          continue

        # Now we have someone that has answer 'yes' to the terms, but has not been
        # registered in our system, so proceed with registration based on their
        # other answers
        hw = HealthWorker()
        hw.vodacom_phone = vodacom_phone

        answers = {
            'name': None,
            'first_name': None,
            'surname': None,
            'country': 'TZ',
            'facility': None,
            'specialties': [],
            'language': None,
            'mct_registration_number': None,
            'mct_payroll_number': None
          }

        for answer in RegistrationAnswer.objects.filter(msisdn=user.msisdn).all():
          if answer.question == RegistrationStatus.INTRO and answer.answer:
            answers['language'] = answer.answer
          elif answer.question == RegistrationStatus.CADRE and answer.answer:
            try:
              Specialty.objects.get(id=int(answer.answer))
              answers['specialties'].append(int(answer.answer))
            except ObjectDoesNotExist:
              pass
          elif answer.question == RegistrationStatus.CHECK_NUMBER and answer.answer:
           answers['mct_payroll_number'] = answer.answer
          elif answer.question == RegistrationStatus.REGISTRATION_NUMBER and answer.answer:
            answers['mct_registration_number'] = answer.answer
          elif answer.question == RegistrationStatus.FIRST_NAME and answer.answer:
            answers['first_name'] = answer.answer
          elif answer.question == RegistrationStatus.LAST_NAME and answer.answer:
            answers['surname'] = answer.answer
          elif answer.question == RegistrationStatus.FACILITY_SELECT and answer.answer:
            try:
              Facility.objects.get(id=int(answer.answer))
              answers['facility'] = int(answer.answer)
            except ObjectDoesNotExist:
              pass
          elif answer.question == RegistrationStatus.SELECT_SPECIALTY and answer.answer:
            try:
              Specialty.objects.get(id=int(answer.answer))
              answers['specialties'].append(int(answer.answer))
            except ObjectDoesNotExist:
              pass

        # Massage answers
        answers['name'] = answers['first_name'] + ' ' + answers['surname']

        # Update healthworker
        hw.name = answers['name']
        hw.surname = answers["surname"]
        hw.country = answers["country"]
        hw.facility = answers["facility"]
        for i in answers["specialties"]:
          hw.save()
          hw.specialties.add(i)
        hw.language = answers["language"]
        hw.mct_registration_num = answers["mct_registration_number"]
        hw.mct_payroll_num = answers["mct_payroll_number"]

        # Save and autoverify
        hw.save()
        hw.auto_verify()
        num_registrations += 1

    print "Summary:"
    print "Num attempts: %d" % num_attempts
    print "Num registrations: %d" % num_registrations
