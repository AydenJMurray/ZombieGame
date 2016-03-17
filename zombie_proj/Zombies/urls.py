from django.conf.urls import patterns, url
from Zombies import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^game_page/$', views.game_page, name='game_page'),
        url(r'^leaderboards/$', views.leaderboard, name='leaderboards'),
        url(r'^start/', views.start, name = 'start'),

        url(r'^user/(?P<user_name>[A-Za-z_/,\.-0-9]+)/$', views.userProfile, name = 'userProfile' ),
        )
