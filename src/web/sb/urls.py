from django.conf.urls import patterns, include, url
from ajax_select import urls as ajax_select_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # main routes
  url(r'^$', 'sb.views.home', name='home'),
  url(r'^cug$', 'sb.healthworker.views.cug', name='home'),
  url(r'^api/1.0/', include('sb.healthworker.urls')),

  # admin docs
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # admin site
  url(r'^admin/lookups/', include(ajax_select_urls)),
  url(r'^admin/', include(admin.site.urls)),
)
