from django.contrib import admin
from sb.healthworker import models

admin.site.register(models.Facility)
admin.site.register(models.FacilityType)
admin.site.register(models.HealthWorker)
admin.site.register(models.MCTRegistration)
admin.site.register(models.MCTPayroll)
admin.site.register(models.Region)
admin.site.register(models.RegionType)
admin.site.register(models.Specialty)
