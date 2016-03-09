from django.conf.urls import patterns, url
from Zombies import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^login', views.login, name='login')
        )