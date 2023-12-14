from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import RedirectView
from django.views.i18n import set_language
from .views import GetUserView, LogoutView, RegisterView, LoginView, logout_view

urlpatterns = [
    path('login-view/', LoginView.as_view(), name="login"),
    path('logout-view/', logout_view),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set-language/', set_language, name='set_language'),

]

urlpatterns += [
    path('', RedirectView.as_view(url='/i18n/', permanent=True)),
]
