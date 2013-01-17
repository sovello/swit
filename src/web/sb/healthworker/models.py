# Copyright 2012 Switchboard, Inc

from django.db import models

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
  other_phone = models.CharField(max_length=255, null=True, blank=True)
  specialties = models.ManyToManyField("Specialty")
  updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
  vodacom_phone = models.CharField(null=True, max_length=128, blank=True)

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

