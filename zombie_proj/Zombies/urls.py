from django.conf.urls import patterns, url
from Zombies import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^game_page/$', views.game_page, name='game_page'),
        url(r'^leaderboards/$', views.leaderboard, name='leaderboards'),
        url(r'^start/', views.start, name = 'start'),

        url(r'^user/(?P<user_name>[A-Za-z_/,\.-0-9]+)/$', views.userProfile, name = 'userProfile' ),
        )
