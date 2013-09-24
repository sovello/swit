import csv
from django.contrib import admin
from django.http import HttpResponse
from sb.healthworker import models

def fmt_date(x):
  if isinstance(x, datetime.datetime):
    return x.strftime('%Y-%m-%d %H:%M:%S')
  elif isinstance(x, datetime.date):
    return x.strftime('%Y-%m-%d')
  else:
    return u''

# http://djangosnippets.org/snippets/2369/
def export_as_csv_action(description="CSV Export", fields=None, exclude=None, header=True):
  """
  This function returns an export csv action
  'fields' and 'exclude' work like in django ModelForm
  'header' is whether or not to output the column names as the first row
  """
  def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    opts = modeladmin.model._meta
    field_names = set([field.name for field in opts.fields])
    if fields:
      fieldset = set(fields)
      field_names = field_names & fieldset
    elif exclude:
      excludeset = set(exclude)
      field_names = field_names - excludeset

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)

    if header:
      writer.writerow(list(field_names))

    for obj in queryset:
      row = []
      for field in field_names:
        value = getattr(obj, field) if hasattr(obj, field) else getattr(modeladmin, field)(obj)
        row.append(unicode(value).encode('utf-8'))
      writer.writerow(row)

    return response

  export_as_csv.short_description = description
  return export_as_csv

class RegionAdmin(admin.ModelAdmin):
  list_display = ["title", "type", "parent_region", "created_at", "updated_at", "subregions"]
  search_fields = ["title"]

  def parent_title(self, o):
    return o.parent_region.title

  def subregions(self, o):
    return ', '.join(m.title for m in models.Region.objects.filter(parent_region=o).all())

class FacilityAdmin(admin.ModelAdmin):
  list_display = ["title", "address", "owner", "msisdn", "is_user_submitted", "type", "show_region_url", "created_at", "updated_at"]
  search_fields = ["title", "owner", "address"]

  def show_region_url(self, facility):
    r = facility.region
    if r:
      return u'<a href="%s">%s</a>' % ('/admin/healthworker/region/%d' % r.id, r.title)
    else:
      return u''
  show_region_url.allow_tags = True
  show_region_url.short_description = 'Region'

class SpecialtyAdmin(admin.ModelAdmin):
  list_display = ["title", "msisdn", "is_user_submitted", "created_at", "updated_at"]
  search_fields = ["title", "msisdn"]

class MCTPayrollAdmin(admin.ModelAdmin):
  list_display = ["name", "last_name", "designation", "birthdate", "check_number", "district", "health_worker", "specialty", "facility",  "region"]
  search_fields = ["name", "last_name", "designation", "birthdate", "check_number", "district"]

class MCTRegistrationAdmin(admin.ModelAdmin):
  list_display = ["name", "address", "birthdate", "cadre", "category", "country", "current_employer", "dates_of_registration_full", "dates_of_registration_temporary", "dates_of_registration_provisional", "email", "employer_during_internship", "facility", "file_number", "health_worker", "qualification_final", "qualification_provisional", "qualification_specialization_1", "qualification_specialization_2", "registration_number", "registration_type", "specialty", "specialty_duration", "created_at", "updated_at"]
  search_fields = ["name", "address", "birthdate", "cadre", "category", "country", "current_employer", "dates_of_registration_full", "dates_of_registration_temporary", "dates_of_registration_provisional", "email", "employer_during_internship", "file_number", "qualification_final", "qualification_provisional", "qualification_specialization_1", "qualification_specialization_2", "registration_number", "registration_type", "specialty_duration"]

class DMORegistrationAdmin(admin.ModelAdmin):
  list_display = ["name", "phone_number", "email", "registration_type", "registration_number", "check_number", "cadre", "city", "district", "region", "gender", "nationality", "duty_station", "department"]
  search_fields = ["name", "phone_number", "registration_number", "check_number", "cadre", "city", "district", "region"]

class HealthWorkerAdmin(admin.ModelAdmin):
  def specialties(self, hw):
    u', '.join([s.title for s in hw.specialties.all()])

  def facility(self, hw):
    hw.facility.title if hw.facility else u''

  def birthday(self, hw):
    fmt_date(hw.birthdate)

  def created(self, hw):
    fmt_date(hw.created_at)

  list_display = ["name", "created_at", "updated_at", "mct_registration_num", "mct_payroll_num", "email", "verification_state", "vodacom_phone", "is_closed_user_group", "request_closed_user_group_at", "added_to_closed_user_group_at"]
  search_fields = ["name", "vodacom_phone", "email", "mct_registration_num", "mct_payroll_num"]
  csv_fields = ["id", "name", "specialties", "facility", "birthday", "address", "vodacom_phone", "is_closed_user_group", "gender", "email", "mct_registration_num", "mct_payroll_num", "verification_state", "created"]
  actions = [export_as_csv_action(fields=csv_fields)]

class RegistrationStatusAdmin(admin.ModelAdmin):
  list_display = ["msisdn", "last_state", "num_ussd_sessions", "num_possible_timeouts", "registered"]
  search_fields = ["msisdn", "last_state", "num_ussd_sessions", "num_possible_timeouts", "registered"]

class RegistrationAnswerAdmin(admin.ModelAdmin):
  list_display = ["msisdn", "question", "answer", "page"]
  search_fields = ["msisdn", "question"]

admin.site.register(models.Facility, FacilityAdmin)
admin.site.register(models.FacilityType)
admin.site.register(models.HealthWorker, HealthWorkerAdmin)
admin.site.register(models.MCTRegistration, MCTRegistrationAdmin)
admin.site.register(models.MCTPayroll, MCTPayrollAdmin)
admin.site.register(models.DMORegistration, DMORegistrationAdmin)
admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.RegionType)
admin.site.register(models.Specialty, SpecialtyAdmin)
admin.site.register(models.RegistrationStatus, RegistrationStatusAdmin)
admin.site.register(models.RegistrationAnswer, RegistrationAnswerAdmin)
