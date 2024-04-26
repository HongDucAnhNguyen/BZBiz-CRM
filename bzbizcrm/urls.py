"""bzbizcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import (LogoutView, LoginView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import path, include
from leads.views import HomePageView, SignupView, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view()),
    path('leads/', include("leads.urls", namespace="leads")),
    path('agents/', include("agents.urls", namespace="agents")),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignupView.as_view(), name="signup"),
    # this url serves the form for the user to enter their email, through which they will receive
    # the link to reset their password
    path('reset-password/', PasswordResetView.as_view(), name="reset-password"),

    # user is redirected to this url after submitting the email
    path('reset-password-done/', PasswordResetDoneView.as_view(), name="password_reset_done"),

    # user can go to this url after getting the reset password email in their inbox
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    # user is redirected to this url after completing the reset process
    path('reset-password-complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
