"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import contextlib
from django.test import TestCase

from sb.healthworker.models import HealthWorker
from sb.healthworker.models import MCTRegistration
from sb.healthworker.models import DMORegistration
from sb.healthworker.models import NGORegistration
from sb.healthworker.models import MCTPayroll

class AutoVerifyTest(TestCase):
  def test_registration_number(self):
    # number and name match MCTRegistration (success)
    with temp_obj(HealthWorker, mct_registration_num='1234', surname='Bickford') as hw, \
        temp_obj(MCTRegistration, registration_number='1234', name='Brandon Bickford') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_REGISTRATION_VERIFIED)

    # number and name match DMORegistration (success)
    with temp_obj(HealthWorker, mct_registration_num='1234', surname='Bickford') as hw, \
        temp_obj(DMORegistration, registration_number='1234', name='Brandon Bickford') as dmo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_REGISTRATION_VERIFIED)

    # number and name match NGORegistration (success)
    with temp_obj(HealthWorker, mct_registration_num='1234', surname='Bickford') as hw, \
        temp_obj(NGORegistration, registration_number='1234', name='Brandon Bickford') as ngo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_REGISTRATION_VERIFIED)

    # surname mismatch
    with temp_obj(HealthWorker, mct_registration_num='1234', surname='Bickford') as hw, \
       temp_obj(MCTRegistration, registration_number='1234', name='Brandon Johnson') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    # surname close enough
    with temp_obj(HealthWorker, mct_registration_num='1234', surname='Bickford') as hw, \
       temp_obj(MCTRegistration, registration_number='1234', name='Brandon Bickfords') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_REGISTRATION_VERIFIED)

    # number mismatch
    with temp_obj(HealthWorker, mct_registration_num='1235', surname='Bickford') as hw, \
       temp_obj(MCTRegistration, registration_number='1234', name='Brandon Bickford') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

  def test_payroll_number(self):
    # number matches MCTPayroll (success)
    with temp_obj(HealthWorker, mct_payroll_num='4567') as hw, \
        temp_obj(MCTPayroll, check_number='4567') as payroll:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_PAYROLL_VERIFIED)

    # number matches DMORegistration (success)
    with temp_obj(HealthWorker, mct_payroll_num='4567') as hw, \
        temp_obj(DMORegistration, check_number='4567') as dmo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_PAYROLL_VERIFIED)

    # number matches NGORegistration (success)
    with temp_obj(HealthWorker, mct_payroll_num='4567') as hw, \
        temp_obj(NGORegistration, check_number='4567') as ngo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.MCT_PAYROLL_VERIFIED)

    # number doesn't match
    with temp_obj(HealthWorker, mct_payroll_num='4567') as hw, \
        temp_obj(MCTPayroll, check_number='1111') as payroll:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

  def test_phone_number(self):
    # number matches DMORegistration (success)
    with temp_obj(HealthWorker, vodacom_phone='255768328988') as hw, \
        temp_obj(DMORegistration, phone_number='255768328988') as dmo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.PHONE_NUMBER_VERIFIED)

    # number matches NGORegistration (success)
    with temp_obj(HealthWorker, vodacom_phone='255768328988') as hw, \
        temp_obj(NGORegistration, phone_number='255768328988') as ngo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.PHONE_NUMBER_VERIFIED)

    # number doesn't match
    with temp_obj(HealthWorker, vodacom_phone='255768328988') as hw, \
        temp_obj(MCTPayroll, check_number='255111111111') as payroll:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

  def test_name(self):
    # name match MCTRegistration (success)
    with temp_obj(HealthWorker, name='Brandon Bickford') as hw, \
        temp_obj(MCTRegistration, name='Brandon Bickford') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.NAME_VERIFIED)

    # name match DMORegistration (success)
    with temp_obj(HealthWorker, name='Brandon Bickford') as hw, \
        temp_obj(DMORegistration, name='Brandon Bickford') as dmo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.NAME_VERIFIED)

    # name match NGORegistration (success)
    with temp_obj(HealthWorker, name='Brandon Bickford') as hw, \
        temp_obj(NGORegistration, name='Brandon Bickford') as dmo:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.NAME_VERIFIED)

    # name mismatch
    with temp_obj(HealthWorker, name='Jim Johnson') as hw, \
       temp_obj(MCTRegistration, name='Brandon Bickford') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    # numeric name
    with temp_obj(HealthWorker, name='1111 2222') as hw, \
       temp_obj(MCTRegistration, name='1111 2222') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    # can't match the same token twice
    with temp_obj(HealthWorker, name='Boniface Boniface') as hw, \
       temp_obj(MCTRegistration, name='Boniface Boaz Daudi') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    # initials in source string not considered
    with temp_obj(HealthWorker, name='J P') as hw, \
       temp_obj(MCTRegistration, name='J P Morgan') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    # initials in dest string not considered
    with temp_obj(HealthWorker, name='Jo Morgan') as hw, \
       temp_obj(MCTRegistration, name='J Morgan') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.UNVERIFIED)

    # name close enough
    with temp_obj(HealthWorker, name='Brandon Bicford') as hw, \
       temp_obj(MCTRegistration, name='Brandon Bickford') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.NAME_VERIFIED)

    # names in different order ok too
    with temp_obj(HealthWorker, name='Brandon Samson Bickford') as hw, \
       temp_obj(MCTRegistration, name='Bickford Brandon Samson') as mct:
      hw.auto_verify()
      self.assertEqual(hw.verification_state, HealthWorker.NAME_VERIFIED)

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

