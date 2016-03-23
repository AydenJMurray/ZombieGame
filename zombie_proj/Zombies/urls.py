from django.conf.urls import patterns, url
from Zombies import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^game_page/$', views.game_page, name='game_page'),
        url(r'^leaderboards/$', views.leaderboard, name='leaderboards'),
        url(r'^start/', views.start, name = 'start'),
        url(r'^turn/(?P<turn>[A-Z]+)/(?P<pos>[0-9]+)/', views.turn, name = 'turn'),
        url(r'^user/(?P<user_name>[A-Za-z_/,-\.0-9]+)/$', views.userProfile, name = 'userProfile' ),
        url(r'^edit/$', views.edit_badges, name = 'badgeEditor'),
        url(r'^add/$', views.add_user, name='addUser'),
        url(r'^new/$', views.new, name = 'newGame'),
        url(r'^help/$', views.howto, name = 'help')

        )
