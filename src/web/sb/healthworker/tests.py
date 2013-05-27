"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import contextlib
from django.test import TestCase

from sb.healthworker.models import HealthWorker
from sb.healthworker.models import MCTRegistration
from sb.healthworker.models import MCTPayroll

class AutoVerifyTest(TestCase):
  def test_auto_verify(self):
    with temp_obj(HealthWorker, email='bickfordb@gmail.com') as hw:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    with temp_obj(HealthWorker, email='bickfordb@gmail.com', mct_registration_num='1234') as hw, \
        temp_obj(MCTRegistration, registration_number='1234') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_REGISTRATION_VERIFIED)

    with temp_obj(HealthWorker, email='bickfordb@gmail.com', mct_registration_num='1235') as hw, \
       temp_obj(MCTRegistration, registration_number='1234') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    with temp_obj(HealthWorker, email='bickfordb@gmail.com', mct_registration_num='1234', mct_payroll_num='4567') as hw, \
        temp_obj(MCTPayroll, check_number='4567') as payroll:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_PAYROLL_VERIFIED)

    with temp_obj(HealthWorker, email='bickfordb@gmail.com', mct_registration_num='1234', mct_payroll_num='4567') as hw, \
       temp_obj(MCTPayroll, check_number='4567') as payroll, \
       temp_obj(MCTRegistration, registration_number='1234') as reg:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_REGISTRATION_VERIFIED)

@contextlib.contextmanager
def temp_obj(django_type, **attrs):
  o = django_type()
  for key, attr in attrs.iteritems():
    setattr(o, key, attr)
  o.save()
  try:
    yield o
  except Exception, e0:
    try:
      o.delete()
    except Exception, delete_exception:
      # Ignore delete exceptions:
      pass
    raise e0
  else:
    o.delete()

