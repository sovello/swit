"Health Worker module URL routes"
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  # List cadres
  url('^cadres', 'sb.healthworker.views.on_cadre_index'),
  url('^facilities', 'sb.healthworker.views.on_facility_index'),
  url('^regions', 'sb.healthworker.views.on_region_index'))

