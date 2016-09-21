from django.conf.urls import include, url
from django.contrib import admin
from listr import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^listr/', include('listr.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

