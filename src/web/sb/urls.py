from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sb.views.home', name='home'),
    url(r'^cug$', 'sb.healthworker.views.cug', name='home'),
    # url(r'^sb/', include('sb.foo.urls')),
    url(r'^api/1.0/', include('sb.healthworker.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
