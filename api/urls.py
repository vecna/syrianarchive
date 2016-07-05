from django.conf.urls import patterns, url
from .views import Database

urlpatterns = patterns('',
  url(r'^database/$', Database.as_view(), name='incident'),
)

