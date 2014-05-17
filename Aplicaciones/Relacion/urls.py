from django.conf.urls import patterns, include, url
from .views import RelacionView
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^$', RelacionView.as_view(), name="item"),


    )