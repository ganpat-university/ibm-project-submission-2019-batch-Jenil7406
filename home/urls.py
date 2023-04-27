from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("findevents",views.find_events, name="find_events"),
    # path("settings",views.settings, name="settings"),
    path("login",views.login_user, name="login"),
    path("logout",views.logout_user, name="logout"),

]
