__author__ = 'kdenny'

from django.conf.urls import url, include
from django.views import generic
from listr.models import Place, List

from listr.views import PlacesList

from listr import views



urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^api/$', views.api_examples, name='api'),

    url(r'^lists/$', views.lists, name='lists'),
    url(r'^new_list/$', views.new_list, name='new_list'),

    url(r'^places/$', views.places_list, name='places_list'),

    url(r'^instagram/$', views.instagram, name='instagram'),
    url(r'^instagram_login/$', views.instagram_login, name='instagram_login'),
    url(r'^instagramUser/$', views.instagramUser, name='instagramUser'),
    url(r'^twitter/$', views.twitter, name='twitter'),
    url(r'^twitter_login/$', views.twitter_login, name='twitter_login'),
    url(r'^facebook_login/$', views.facebook_login, name='facebook_login'),
    url(r'^facebook/$', views.facebook, name='facebook'),
    url(r'^google_login/$', views.google_login, name='google_login'),
    url(r'^google/$', views.googlePlus, name='googlePlus'),
    url(r'^(?P<pk>[0-9]+)/$', PlacesList.as_view(),
        name='place_list')
]


