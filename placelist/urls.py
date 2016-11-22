from django.conf.urls import include, url
from django.contrib import admin
from listr import views

from listr.api import ListResource

list_resource = ListResource()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^listr/', include('listr.urls')),
    url(r'^api/', include(list_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
]

