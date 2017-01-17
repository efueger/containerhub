# coding: utf-8

from django.conf.urls import url

from . import views

app_name = 'welcome'
urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
]