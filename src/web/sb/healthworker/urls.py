"Health Worker module URL routes"
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  # List cadres
  url('^specialties', 'sb.healthworker.views.on_specialty_index'),
  url('^mct-registrations', 'sb.healthworker.views.on_mct_registration_index'),
  url('^mct-payrolls', 'sb.healthworker.views.on_mct_payroll_index'),
  url('^facilities', 'sb.healthworker.views.on_facility_index'),
  url('^health-workers', 'sb.healthworker.views.on_health_worker'),
  url('^regions', 'sb.healthworker.views.on_region_index'))

