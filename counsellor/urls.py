from django.conf.urls import patterns, include, url
from django.contrib import admin

from app.mmGrid.urls import grid_patterns
from app.urls import counsellor_patterns
from app.views import login

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin', include(admin.site.urls)),
                       url(r'^', include(counsellor_patterns)),
                       url(r'^', include(grid_patterns)),
                       url(r'', login),
                       )
