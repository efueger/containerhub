from django.conf.urls import url

from . import views


app_name = 'hub'
urlpatterns = [
    # ex: /profile/
    url(r'^profile/$', views.profile, name='profile'),
    # ex: /profile/5/
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    # ex: /hub/5/results/
    #url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /hub/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
