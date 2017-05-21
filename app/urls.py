from django.conf.urls import patterns, url
from app import views

counsellor_patterns = patterns(
    'app.views',
    url(r'^$', 'index_main', name='index_main'),
    url(r'index_main^$', 'index_main', name='index_main'),
    url(r'bulletin_board$', 'bulletin_board', name='bulletin_board'),
    url(r'message$', 'message', name='message'),
    url(r'counsellor$', 'counsellor', name='counsellor'),
    url(r'login$', 'login', name='login'),
    url(r'^register$', 'register', name='register'),
    url(r'^index$', 'index', name='index'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^main$', 'main', name='main'),
    url(r'^modify_pwd$', 'modify_pwd', name='modify_pwd'),
    url(r'^my_profile$', 'my_profile', name='my_profile'),
    url(r'^menu$', 'menu', name='menu')
)
