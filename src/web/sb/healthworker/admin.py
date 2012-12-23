from django.contrib import admin
from sb.healthworker import models

admin.site.register(models.Facility)
admin.site.register(models.FacilityType)
admin.site.register(models.HealthWorker)
admin.site.register(models.MCTRegistration)
admin.site.register(models.MCTPayroll)

class RegionAdmin(admin.ModelAdmin):

  list_display = ["title", "type", "parent_region", "created_at", "updated_at", "subregions"]
  search_fields = ["title"]

  def parent_title(self, o):
    return o.parent_region.title

  def subregions(self, o):
    return ', '.join(m.title for m in models.Region.objects.filter(parent_region=o).all())

admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.RegionType)
admin.site.register(models.Specialty)
