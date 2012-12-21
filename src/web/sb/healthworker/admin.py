from django.contrib import admin
from sb.healthworker import models

class CadreAdmin(admin.ModelAdmin):
  list_display = ['title', 'created_at', 'updated_at']

admin.site.register(models.Cadre, CadreAdmin)
admin.site.register(models.Facility)
admin.site.register(models.FacilityType)
admin.site.register(models.HealthWorker)
admin.site.register(models.MCTRegistrationNumber)
admin.site.register(models.Region)
admin.site.register(models.RegionType)
admin.site.register(models.Specialty)
