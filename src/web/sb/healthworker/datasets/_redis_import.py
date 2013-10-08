import json
import re

from django.db import transaction

from sb.healthworker.datasets import _helpers
from sb.healthworker.models import RegistrationStatus, RegistrationAnswer

# Mapping from state names to our integer ids
def _lookup_state(state_name):
  return {
    'intro': RegistrationStatus.INTRO,
    'no_vodacom_sim': RegistrationStatus.NO_VODACOM_SIM,
    'cadre': RegistrationStatus.CADRE,
    'cadre_other': RegistrationStatus.CADRE_OTHER,
    'cadre_unavailable': RegistrationStatus.CADRE_UNAVAILABLE,
    'cadre_unavailable_contact': RegistrationStatus.CADRE_UNAVAILABLE_CONTACT,
    'cadre_unavailable_dont_contact': RegistrationStatus.CADRE_UNAVAILABLE_DONT_CONTACT,
    'cheque_number': RegistrationStatus.CHECK_NUMBER,
    'registration_number': RegistrationStatus.REGISTRATION_NUMBER,
    'date_of_birth': RegistrationStatus.DATE_OF_BIRTH,
    'dont_match_mct': RegistrationStatus.DONT_MATCH_MCT,
    'dont_match_mct_end': RegistrationStatus.DONT_MATCH_MCT_END,
    'first_name': RegistrationStatus.FIRST_NAME,
    'surname': RegistrationStatus.LAST_NAME,
    'terms_and_conditions': RegistrationStatus.TERMS,
    'session1_end': RegistrationStatus.SESSION1_END,
    'session1_abort_yn': RegistrationStatus.SESSION1_ABORT_YN,
    'session1_abort': RegistrationStatus.SESSION1_ABORT,
    'session2_intro': RegistrationStatus.SESSION2_INTRO,
    'district_select': RegistrationStatus.DISTRICT_SELECT,
    'district_reenter': RegistrationStatus.DISTRICT_REENTER,
    'facility_type': RegistrationStatus.FACILITY_TYPE,
    'facility_name': RegistrationStatus.FACILITY_NAME,
    'facility_select': RegistrationStatus.FACILITY_SELECT,
    'select_speciality': RegistrationStatus.SELECT_SPECIALTY,
    'email': RegistrationStatus.EMAIL,
    'session2_end': RegistrationStatus.SESSION2_END,
    'end': RegistrationStatus.END
  }.get(state_name)

def import_user_progress(user):
  # Most of the information is in a json-encoded value
  key = user.get('key', '')
  value = user.get('value', '')

  # Extract msisdn. Look for a key named "key" with a value like "users.+255752036824"
  match = re.match(r'^users\.\+(\d+)$', key)
  if not match:
    return # there are other records we don't care about
  msisdn = match.group(1)

  # Decode value
  if value == '':
    return
  user = json.loads(value)

  print("Importing user %s: %s" % (msisdn, user))

  # Get or create RegistrationStatus
  status = _helpers.first(RegistrationStatus.objects.filter(msisdn=msisdn))
  if status is None:
    status = RegistrationStatus()
    status.msisdn = msisdn
  status.last_state = _lookup_state(user.get('current_state'))
  status.num_ussd_sessions = user.get('custom', {}).get('ussd_sessions')
  status.num_possible_timeouts = user.get('custom', {}).get('possible_timeouts')
  status.registered = user.get('custom', {}).get('registered', False)
  status.save()

  # Import answers
  for k in user.get('answers', {}).keys():
    state = _lookup_state(k)
    if state is None:
      print("Unknown state found in answers: %s" % k)

    answer = _helpers.first(RegistrationAnswer.objects.filter(msisdn=msisdn, question=state))
    if answer is None:
      answer = RegistrationAnswer()
      answer.msisdn = msisdn
      answer.question = state
    if user['answers'][k] is not None:
      answer.answer = user['answers'][k]
    answer.save()

  # Import pages. Some questions are multi-page and this tells us which page
  # they last saw. We do this separately because it's possible to have a page and
  # not an answer
  for k in user.get('pages', {}).keys():
    state = _lookup_state(k)
    if state is None:
      print("Unknown state found in pages: %s" % k)

    answer = _helpers.first(RegistrationAnswer.objects.filter(msisdn=msisdn, question=state))
    if answer is None:
      answer = RegistrationAnswer()
      answer.msisdn = msisdn
      answer.question = state
    if user['pages'][k] is not None:
      answer.page = user['pages'][k]
    answer.save()

def import_redis_backup(path):
  data = _helpers.read_lf_json(path)
  with transaction.commit_on_success():
    for user in data:
      import_user_progress(user)

