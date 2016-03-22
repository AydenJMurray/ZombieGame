from django.conf.urls import patterns, include, url
from django.contrib import admin
from Zombies.models import Player
from Zombies.views import home

from django.contrib.auth import authenticate
from django.contrib.auth import login

from registration import signals
from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
	def get_success_url(self, request):
		return '/accounts/register/complete/'

    #Overriden method from django-registration-redux so that when a user is created, a corresponding player is created
	def register(self, form):
		new_user = form.save()
		username_field = getattr(new_user, 'USERNAME_FIELD', 'username')
		new_user = authenticate(
			username=getattr(new_user, username_field),
			password=form.cleaned_data['password1']
		)

		login(self.request, new_user)
		signals.user_registered.send(sender=self.__class__,
									 user=new_user,
									 request=self.request)

		p = Player.objects.get_or_create(user=new_user)[0]
		p.save()
		return new_user


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^Zombies/', include('Zombies.urls')),
	url(r'^', include('Zombies.urls')),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)
