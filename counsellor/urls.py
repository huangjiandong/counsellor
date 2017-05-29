# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from app.news.urls import news_patterns
from app.messages.urls import messages_patterns
from app.users.urls import users_patterns
from app.urls import counsellor_patterns
from app.views import login

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin', include(admin.site.urls)),
                       url(r'^', include(counsellor_patterns)),
                       url(r'^', include(news_patterns)),
                       url(r'^', include(messages_patterns)),
                       url(r'^', include(users_patterns)),
                       url(r'', login),
                       )
