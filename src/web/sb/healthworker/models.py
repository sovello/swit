# Copyright 2012 Switchboard, Inc

from django.db import models

class HealthWorker(models.Model):
  address = models.TextField(null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  cadre = models.ForeignKey("Cadre", null=True, blank=True)
  country = models.CharField(max_length=2, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  email = models.EmailField(null=True, blank=True)
  facility = models.ForeignKey("Facility", null=True, blank=True)
  gender = models.CharField(max_length=16, choices=[("male", "Male"), ("female", "Female")], null=False)
  mct_category = models.CharField(max_length=255, null=True, blank=True)
  mct_current_employer = models.CharField(max_length=255, null=True, blank=True)
  mct_dates_of_registration_full = models.CharField(max_length=255, null=True, blank=True)
  mct_dates_of_registration_provisional = models.CharField(max_length=255, null=True, blank=True)
  mct_dates_of_registration_temporary = models.CharField(max_length=255, null=True, blank=True)
  mct_employer_during_internship = models.CharField(max_length=255, null=True, blank=True)
  mct_file_number = models.CharField(max_length=255, null=True, blank=True)
  other_phone = models.CharField(max_length=255, null=True, blank=True)
  mct_qualification_final = models.CharField(max_length=255, null=True, blank=True)
  mct_qualification_provisional = models.CharField(max_length=255, null=True, blank=True)
  mct_qualification_specialization_1 = models.CharField(max_length=255, null=True, blank=True)
  mct_qualification_specialization_2 = models.CharField(max_length=255, null=True, blank=True)
  mct_specialty = models.CharField(max_length=255, null=True, blank=True)
  mct_specialty_duration = models.CharField(max_length=255, null=True, blank=True)
  name = models.CharField(max_length=255, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  vodacom_phone = models.CharField(null=True, max_length=128, blank=True)

  # This improves the Django admin view:
  def __unicode__(self):
    return self.name

class Cadre(models.Model):
  """A health worker cadre

  I think this is along the lines of "Doctor" or "Nurse" but I"m not certain
  """
  abbreviation = models.CharField(max_length=32, null=False, blank=False, unique=True)
  title = models.CharField(max_length=255, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class DistrictType(models.Model):
  "The type of a district like 'Village'"
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class Region(models.Model):
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class District(models.Model):
  "A district like 'The Bronx'"
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  region = models.ForeignKey(Region, null=True, blank=True, db_index=True)
  type = models.ForeignKey(DistrictType, null=True, blank=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class FacilityType(models.Model):
  "A facility type like Hospital"
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

  def __unicode__(self):
    return self.title

class Facility(models.Model):
  """A facility where health workers work

  Like "Dar Es Salam Medical Center"
  """
  title = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  district = models.ForeignKey(District, null=True, blank=True, db_index=True)
  address = models.TextField(blank=True, null=True)
  email = models.CharField(max_length=255, blank=True, null=True)
  owner = models.CharField(max_length=255, blank=True, null=True)
  ownership_type = models.CharField(max_length=255, blank=True, null=True)
  phone = models.CharField(max_length=255, blank=True, null=True)
  place_type = models.CharField(max_length=64, blank=True, null=True, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  type = models.ForeignKey(FacilityType, null=False, blank=False, db_index=True)

  def __unicode__(self):
    return self.title

class Specialty(models.Model):
  """A health worker specialty

  Like "Brain Transplant Surgery"
  """
  title = models.CharField(max_length=255, blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  parent_specialty = models.ForeignKey("Specialty", blank=True, null=True)

  def __unicode__(self):
    return self.title

class MCTRegistrationNumber(models.Model):
  """Tanzanian Ministry of Health Registration number
  """
  number = models.CharField(max_length=255, null=False, blank=False, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  health_worker = models.ForeignKey("HealthWorker", blank=True, null=True, db_index=True)

  def __unicode__(self):
    return self.number
