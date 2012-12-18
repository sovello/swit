"Health Worker module URL routes"
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  # List cadres
  url('^cadres', 'sb.healthworker.views.on_cadre_index'))

