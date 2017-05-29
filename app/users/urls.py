# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

users_patterns = patterns(
    'app.users.views',
    url(r'users$', 'get_users', name='users'),
    url(r'users_edit$', 'users_edit', name='users_edit'),
)
