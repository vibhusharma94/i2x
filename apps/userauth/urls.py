from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from apps.userauth import views as auth_views

urlpatterns = [
    url(r'^login/$', csrf_exempt(auth_views.LoginView.as_view()), name='api_login_url'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='api_logout_url'),
    url(r'^signup/$', auth_views.SignupView.as_view(), name='api_signup_url'),
    url(r'^refresh/token/$', auth_views.RefreshTokenView.as_view(), name='api_refresh_token'),
    url(r'^forgot-password/$', auth_views.PasswordResetRequestKey.as_view(), name='forgot_password_url'),
    url(r'^reset-password/(?P<key>.+)/$', auth_views.PasswordResetFromKey.as_view(), name='reset_password_url'),
    url(r'^email-verification/(?P<key>.+)/$', auth_views.EmailVerificationKey.as_view(), name='email_verification_url'),

]
