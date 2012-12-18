# Copyright 2012 Switchboard, Inc

from django.db import models

# Create your models here.
class HealthWorker(models.Model):
  name = models.CharField(max_length=255, null=False, blank=False)
  _gender_options = [("male", "Male"), ("female", "Female")]
  gender = models.CharField(max_length=16, choices=_gender_options, null=False)
  birthdate = models.DateField(null=True, blank=True)
  # ISO three character country code
  country = models.CharField(max_length=3, null=True, blank=True)
  postal_address = models.TextField(null=True, blank=True)
  vodacom_phone = models.CharField(null=True, max_length=128, blank=True)
  other_phone = models.CharField(null=True, max_length=128, blank=True)
  email = models.EmailField(null=True, blank=True)
  facility = models.ForeignKey('Facility', null=True, blank=True)
  cadre = models.ForeignKey('Cadre', null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  # This improves the Django admin view:
  def __unicode__(self):
    return self.name

class Cadre(models.Model):
  """A health worker cadre

  I think this is along the lines of 'Doctor' or 'Nurse' but I'm not certain
  """
  title = models.CharField(max_length=255, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class DistrictType(models.Model):
  "The type of a district like 'Village'"
  title = models.CharField(max_length=255, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class District(models.Model):
  "A district like 'The Bronx'"
  title = models.CharField(max_length=255, null=False, blank=False)
  type = models.ForeignKey(DistrictType, null=False)
  parent_district = models.ForeignKey("District", null=False, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class FacilityType(models.Model):
  "A facility type like Hospital"
  title = models.CharField(max_length=255, null=False, blank=False)

  def __unicode__(self):
    return self.title

class Facility(models.Model):
  """A facility where health workers work

  Like 'Dar Es Salam Medical Center' (sp!?)
  """
  title = models.CharField(max_length=255, null=False, blank=False)
  district = models.ForeignKey(District, null=True, blank=True)
  address = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  type = models.ForeignKey(FacilityType, null=False, blank=False)

  def __unicode__(self):
    return self.title

class Specialty(models.Model):
  """A health worker specialty

  Like 'Brain Transplant Surgery'
  """
  title = models.CharField(max_length=255, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  parent_specialty = models.ForeignKey("Specialty", blank=True, null=True)

  def __unicode__(self):
    return self.title

class RegistrationNumber(models.Model):
  """Registration number

  I'm not really sure what this is, but I believe it's some sort of government
  issued health worker registration number that Switchboard will use to validate health care workers"""

  registration_number = models.CharField(max_length=255, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  health_worker = models.ForeignKey("HealthWorker", blank=True, null=True)

  def __unicode__(self):
    return self.registration_number
