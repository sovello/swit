# Copyright 2012 Switchboard, Inc

import datetime

from django.db import models

import sb.logchan
import sb.util

CUG_ACTIVATION_SMSES = {
  "en":
    ("Congratulations, you are added to the Health Network Programme!"
     " You can now make free calls and SMSs to other practitioners in"
     " the programme."),
  "sw":
    ("HONGERA! umefanikiwa kujiunga na Mtandao wa watumishi wa Afya"
     " nchini.Sasa unaweza kuongea na kutuma SMS BURE."),
}

CUG_DEACTIVATION_SMSES = {
  "en":
    ("You have been removed from the Health Network Programme and"
     " may no longer make free calls and SMSs to practitioners in"
     " the programme."),
  "sw":
    ("You have been removed from the Health Network Programme and"
     " may no longer make free calls and SMSs to practitioners in"
     " the programme."),  # TODO: translate
}

class HealthWorker(models.Model):
  address = models.TextField(null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  country = models.CharField(max_length=2, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  email = models.EmailField(null=True, blank=True)
  facility = models.ForeignKey("Facility", null=True, blank=True, db_index=True)
  gender = models.CharField(max_length=16, choices=[("male", "Male"), ("female", "Female")], null=True, blank=True)
  language = models.CharField(max_length=32, blank=True, null=True)
  name = models.CharField(max_length=255, null=False, blank=False)
  surname = models.CharField(null=True, max_length=128, blank=True)
  other_phone = models.CharField(max_length=255, null=True, blank=True)
  specialties = models.ManyToManyField("Specialty", blank=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  vodacom_phone = models.CharField(null=True, max_length=128, blank=True)
  mct_registration_num = models.CharField(null=True, max_length=128, blank=True)
  mct_payroll_num = models.CharField(null=True, max_length=128, blank=True)
  is_closed_user_group = models.BooleanField(default=False, blank=True)
  added_to_closed_user_group_at = models.DateTimeField(null=True, default=None, blank=True)
  request_closed_user_group_at = models.DateTimeField(null=True, default=None, blank=True)

  UNVERIFIED = 0
  MCT_PAYROLL_VERIFIED = 1
  MCT_REGISTRATION_VERIFIED = 2
  MANUALLY_VERIFIED = 3

  verification_state = models.IntegerField(default=0,
                                           null=False,
                                           blank=True,
                                           choices=[(UNVERIFIED, u"Needs Verification"),
                                                    (MCT_PAYROLL_VERIFIED, u"Verified By MCT Payroll Number"),
                                                    (MCT_REGISTRATION_VERIFIED, u"Verified By MCT Registration Number+Name"),
                                                    (MANUALLY_VERIFIED, u"Manually Verified")])

  def auto_verify(self):
    if self.verification_state != self.UNVERIFIED:
      return

    if self.mct_payroll_num:
      payrolls = MCTPayroll.objects
      payrolls = payrolls.filter(check_number=self.mct_payroll_num).filter(health_worker_id__isnull=True)
      try:
        payroll = payrolls[0]
        payroll.health_worker = self
        payroll.save()
        self.verification_state = self.MCT_PAYROLL_VERIFIED
        self.save()
      except IndexError:
        pass
    if self.surname and self.mct_registration_num:
      regs = MCTRegistration.objects
      regs = regs.filter(registration_number=self.mct_registration_num).filter(health_worker_id__isnull=True)
      regs = regs.extra(where=["edit_search(%s, healthworker_mctregistration.name, 2)"], params=[self.surname])
      try:
        reg = regs[0]
        reg.health_worker = self
        reg.save()
        self.verification_state = self.MCT_REGISTRATION_VERIFIED
        self.save()
      except IndexError:
        pass

  def set_closed_user_group(self, in_group):
    "Set the closed user group status of a user"
    in_group = bool(in_group)
    if in_group == self.is_closed_user_group:
      return
    if in_group:
      self.send_activation_sms()
    else:
      self.send_deactivation_sms()
    self.is_closed_user_group = in_group
    if in_group:
      self.added_to_closed_user_group_at = datetime.datetime.now()
    else:
      self.added_to_closed_user_group_at = None
    self.save()
    sb.logchan.write("closed-user-group-change",
                     phone=self.vodacom_phone,
                     change=in_group,
                     id=self.id)


  def send_activation_sms(self):
    content = CUG_ACTIVATION_SMSES.get(self.language)
    if not content:
      content = CUG_ACTIVATION_SMSES["en"]
    sb.util.send_vumigo_sms(self.vodacom_phone, content)

  def send_deactivation_sms(self):
    content = CUG_DEACTIVATION_SMSES.get(self.language)
    if content is None:
      content = CUG_DEACTIVATION_SMSES["en"]
    sb.util.send_vumigo_sms(self.vodacom_phone, content)

  # This improves the Django admin view:
  def __unicode__(self):
    return self.name

class RegionType(models.Model):
  """The type of a region like "Village" """
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  COUNTRY = "Country"
  VILLAGE = "Village"
  WARD = "Ward"
  DISTRICT = "District"
  REGION = "Region"
  DIVISION = "Division"

  def __unicode__(self):
    return self.title

class Region(models.Model):
  """A region like "The Bronx" """
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  type = models.ForeignKey(RegionType, null=True, blank=True, db_index=True)
  parent_region = models.ForeignKey("Region", null=True, blank=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

  @classmethod
  def get_or_create_region_by_title_type(cls, title, region_type_title, parent=None, filter_parent=True):
    region_type = get_or_create_by_title(RegionType, region_type_title)
    try:
      if filter_parent:
        return Region.objects.get(title__iexact=title, type=region_type, parent_region=parent)
      else:
        return Region.objects.get(title__iexact=title, type=region_type)
    except Region.DoesNotExist:
      region = Region()
      region.type = region_type
      region.title = title
      region.parent_region = parent
      region.save()
      return region

  def subregion_ids(self):
    result = set()
    parent_region_ids = [self.id]
    while parent_region_ids:
      subregions = list(Region.objects.filter(parent_region_id__in=parent_region_ids).all())
      parent_region_ids = [i.id for i in subregions]
      result.update(parent_region_ids)
    return result

class FacilityType(models.Model):
  "A facility type like Hospital"
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  priority = models.IntegerField(null=False, default=0, blank=True)

  def __unicode__(self):
    return self.title

class Facility(models.Model):
  """A facility where health workers work

  Like "Dar Es Salam Medical Center"
  """
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  region = models.ForeignKey(Region, null=True, blank=True, db_index=True)
  address = models.TextField(blank=True, null=True)
  serial_number = models.CharField(max_length=128, blank=True, null=True, db_index=True)
  email = models.CharField(max_length=255, blank=True, null=True)
  owner = models.CharField(max_length=255, blank=True, null=True)
  ownership_type = models.CharField(max_length=255, blank=True, null=True)
  phone = models.CharField(max_length=255, blank=True, null=True)
  place_type = models.CharField(max_length=64, blank=True, null=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  type = models.ForeignKey(FacilityType, null=True, blank=False, db_index=True)
  msisdn = models.CharField(max_length=255, blank=True, null=True)
  is_user_submitted = models.NullBooleanField()
  latitude = models.FloatField(null=True, blank=True)
  longitude = models.FloatField(null=True, blank=True)
  alternative_names = models.CharField(max_length=255, null=True, blank=True)
  status = models.CharField(max_length=255, null=True, blank=True)
  hmis = models.CharField(max_length=255, null=True, blank=True)
  remarks = models.CharField(max_length=255, null=True, blank=True)
  registration_num = models.CharField(max_length=255, null=True, blank=True)
  source = models.CharField(max_length=255, null=True, blank=True)
  current_id = models.CharField(max_length=255, null=True, blank=True)

  def __unicode__(self):
    return self.title

class Specialty(models.Model):
  """A health worker specialty

  The top level specialties are "cadres"

  Like "Brain Transplant Surgery"
  """
  title = models.CharField(max_length=255, blank=False, null=False, db_index=True)
  abbreviation = models.CharField(max_length=32, blank=True, null=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  parent_specialty = models.ForeignKey("Specialty", blank=True, null=True, db_index=True)
  is_user_submitted = models.NullBooleanField()
  is_query_subspecialties = models.BooleanField(default=False, blank=True)
  msisdn = models.CharField(max_length=255, blank=True, null=True)
  short_title = models.CharField(max_length=255, null=True, blank=True)
  priority = models.IntegerField(default=0, null=False, blank=True)

  def tree(self):
    curr = self
    while curr is not None:
      yield curr
      curr = curr.parent_specialty

  def __unicode__(self):
    return u" -> ".join([i.title for i in reversed(list(self.tree()))])

  def is_child_of(self, ancestor):
    curr = self
    while curr is not None:
      if ancestor.id == curr.parent_specialty_id:
        return True
      curr = curr.parent_specialty
    return False

  @classmethod
  def get_or_create_by_abbreviation(cls, abbrev):
    """Get or create a specialty by an abbreviation"""
    if not abbrev:
      return
    try:
      return Specialty.objects.get(abbreviation__iexact=abbrev)
    except Specialty.DoesNotExist:
      specialty = models.Specialty()
      specialty.abbreviation = abbrev
      specialty.title = abbrev
      specialty.save()
      return specialty

def get_or_create_by_title(model, title):
  if not title:
    return None
  try:
    return model.objects.get(title__iexact=title)
  except model.DoesNotExist:
    o = model()
    o.title = title
    o.save()
    return o

# Data provided by MCT payroll list
class MCTPayroll(models.Model):
  last_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  designation = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  birthdate = models.DateField(max_length=255, null=True, blank=True)
  check_number = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  district = models.CharField(max_length=255, null=True, blank=True)
  health_worker = models.ForeignKey(HealthWorker, null=True, blank=True, db_index=True)
  specialty = models.ForeignKey(Specialty, null=True, blank=True, db_index=True)
  facility = models.ForeignKey(Facility, null=True, blank=True, db_index=True)
  region = models.ForeignKey(Region, null=True, blank=True, db_index=True)

# Data provided by MCT registration list
class MCTRegistration(models.Model):
  address = models.TextField(null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  cadre = models.CharField(max_length=255, null=True, blank=True)
  category = models.CharField(max_length=255, null=True, blank=True)
  country = models.CharField(max_length=2, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  current_employer = models.CharField(max_length=255, null=True, blank=True)
  dates_of_registration_full = models.CharField(max_length=255, null=True, blank=True)
  dates_of_registration_provisional = models.CharField(max_length=255, null=True, blank=True)
  dates_of_registration_temporary = models.CharField(max_length=255, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  employer_during_internship = models.CharField(max_length=255, null=True, blank=True)
  facility = models.ForeignKey("Facility", null=True, blank=True, db_index=True)
  file_number = models.CharField(max_length=255, null=True, blank=True)
  health_worker = models.ForeignKey(HealthWorker, null=True, blank=True, db_index=True)
  name = models.CharField(max_length=255, null=False, blank=False)
  qualification_final = models.CharField(max_length=255, null=True, blank=True)
  qualification_provisional = models.CharField(max_length=255, null=True, blank=True)
  qualification_specialization_1 = models.CharField(max_length=255, null=True, blank=True)
  qualification_specialization_2 = models.CharField(max_length=255, null=True, blank=True)
  registration_number = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  registration_type = models.CharField(max_length=2, null=True, blank=True)
  specialties = models.ManyToManyField("Specialty")
  specialty = models.CharField(max_length=255, null=True, blank=True)
  specialty_duration = models.CharField(max_length=255, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.name

# Data provided by DMO registration list
class DMORegistration(models.Model):
  # Useful for autoverify
  name = models.CharField(max_length=255, null=True, blank=False)
  phone_number = models.CharField(max_length=255, null=True, blank=True)
  registration_type = models.CharField(max_length=2, null=True, blank=True)
  registration_number = models.CharField(max_length=255, null=True, blank=True)
  check_number = models.CharField(max_length=255, null=True, blank=True)
  health_worker = models.ForeignKey(HealthWorker, null=True, blank=True, db_index=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  # Not really used, but import it anyway, might want it at some point
  cadre = models.CharField(max_length=255, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  city = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  district = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  region = models.CharField(max_length=255, null=True, blank=True, db_index=True)
  nationality = models.CharField(max_length=255, null=True, blank=True)
  gender = models.CharField(max_length=255, null=True, blank=True)
  duty_station = models.CharField(max_length=255, null=True, blank=True)
  department = models.CharField(max_length=255, null=True, blank=True)

  def __unicode__(self):
    return self.name

# Data provided by Vumi on the current state of each user
class RegistrationStatus(models.Model):
  # USSD States
  INTRO = 0
  NO_VODACOM_SIM = 1
  CADRE = 2
  CADRE_OTHER = 3
  CADRE_UNAVAILABLE = 4
  CADRE_UNAVAILABLE_CONTACT = 5
  CADRE_UNAVAILABLE_DONT_CONTACT = 6
  CHECK_NUMBER = 7 # cheque_number
  REGISTRATION_NUMBER = 8
  DATE_OF_BIRTH = 9 # this state has been disabled
  DONT_MATCH_MCT = 10
  DONT_MATCH_MCT_END = 11
  FIRST_NAME = 12
  LAST_NAME = 13 # surname
  TERMS = 14 # terms_and_conditions
  SESSION1_END = 15
  SESSION1_ABORT_YN = 16
  SESSION1_ABORT = 17
  SESSION2_INTRO = 18
  DISTRICT_SELECT = 19
  DISTRICT_REENTER = 20
  FACILITY_TYPE = 21
  FACILITY_NAME = 22
  FACILITY_SELECT = 23
  SELECT_SPECIALTY = 24
  EMAIL = 25 # this state has been disabled
  SESSION2_END = 26
  END = 27 # apparently a legacy state, not really used

  USSD_STATES = [
      (INTRO, u"1. Choose Language - Session 1 Intro"),
      (NO_VODACOM_SIM, u"Not a Vodacom Customer (ABORT)"),
      (CADRE, u"2. Choose Cadre"),
      (CADRE_OTHER, u"2a. Enter Other Cadre"),
      (CADRE_UNAVAILABLE, u"2b. Cadre Unavailable"),
      (CADRE_UNAVAILABLE_CONTACT, u"2c. Cadre Unavailable - Please Contact (ABORT)"),
      (CADRE_UNAVAILABLE_DONT_CONTACT, u"2d. Cadre Unavailable - Don't Contact (ABORT)"),
      (CHECK_NUMBER, u"3. Enter Check Number"),
      (REGISTRATION_NUMBER, u"3a. Enter Registration Number"),
      (DATE_OF_BIRTH, u"Enter Date of Birth (LEGACY)"),
      (DONT_MATCH_MCT, u"3b. Info didn't match - try again?"),
      (DONT_MATCH_MCT_END, u"3c. Info didn't match (ABORT)"),
      (FIRST_NAME, u"4. Enter First name"),
      (LAST_NAME, u"5. Enter Last name"),
      (TERMS, u"6. Accept Terms and conditions?"),
      (SESSION1_END, u"7. Session 1 Ended Normally"),
      (SESSION1_ABORT_YN, u"6b. Terms declined. Are you sure?"),
      (SESSION1_ABORT, u"6c. Terms declined (ABORT)"),
      (SESSION2_INTRO, u"8. Enter district - Session 2 Intro"),
      (DISTRICT_SELECT, u"8a. Select district"),
      (DISTRICT_REENTER, u"8b. District unknown, please re-enter"),
      (FACILITY_TYPE, u"9. Select facility type"),
      (FACILITY_NAME, u"10. Enter facility name"),
      (FACILITY_SELECT, u"10a. Select facility"),
      (SELECT_SPECIALTY, u"11. Select speciality"),
      (EMAIL, u"Enter email address (LEGACY)"),
      (SESSION2_END, u"12. Session 2 ended normally"),
      (END, u"End (LEGACY)")]

  msisdn = models.CharField(max_length=255, blank=False, db_index=True, unique=True)
  last_state = models.IntegerField(blank=False, choices=USSD_STATES)
  num_ussd_sessions = models.IntegerField(null=True, blank=True)
  num_possible_timeouts = models.IntegerField(null=True, blank=True)
  registered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

# The individual answers to each question
class RegistrationAnswer(models.Model):
  msisdn = models.CharField(max_length=255, blank=False)
  question = models.IntegerField(blank=False, choices=RegistrationStatus.USSD_STATES)
  answer = models.CharField(max_length=255, blank=True)
  page = models.IntegerField(null=True, blank=True) # some questions are multi-page, this is the last page they saw
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

class DataSet(models.Model):
  key = models.CharField(null=False, blank=False, max_length=128)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

