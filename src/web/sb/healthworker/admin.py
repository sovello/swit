from django.contrib import admin
from sb.healthworker import models

class RegionAdmin(admin.ModelAdmin):
  list_display = ["title", "type", "parent_region", "created_at", "updated_at", "subregions"]
  search_fields = ["title"]

  def parent_title(self, o):
    return o.parent_region.title

  def subregions(self, o):
    return ', '.join(m.title for m in models.Region.objects.filter(parent_region=o).all())

class FacilityAdmin(admin.ModelAdmin):
  list_display = ["title", "address", "owner", "msisdn", "is_user_submitted", "type", "region", "created_at", "updated_at"]
  search_fields = ["title", "owner", "address"]

class MCTPayrollAdmin(admin.ModelAdmin):
  list_display = ["name", "last_name", "designation", "birthdate", "check_number", "district", "health_worker", "specialty", "facility",  "region"]
  search_fields = ["name"]

class MCTRegistrationAdmin(admin.ModelAdmin):
  list_display = ["name", "address", "birthdate", "cadre", "category", "country", "current_employer", "dates_of_registration_full", "dates_of_registration_temporary", "dates_of_registration_provisional", "email", "employer_during_internship", "facility", "file_number", "health_worker", "qualification_final", "qualification_provisional", "qualification_specialization_1", "qualification_specialization_2", "registration_number", "registration_type", "specialty", "specialty_duration", "created_at", "updated_at"]
  search_fields = ["name"]

admin.site.register(models.Facility, FacilityAdmin)
admin.site.register(models.FacilityType)
admin.site.register(models.HealthWorker)
admin.site.register(models.MCTRegistration, MCTRegistrationAdmin)
admin.site.register(models.MCTPayroll, MCTPayrollAdmin)
admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.RegionType)
admin.site.register(models.Specialty)
