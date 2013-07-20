from django.conf.urls import patterns, include, url
from polls import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>\d)+/$', views.PollView.as_view(), name='poll'),
    url(r'^(?P<pk>\d)+/result/$', views.ResultView.as_view(), name='poll_result'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
