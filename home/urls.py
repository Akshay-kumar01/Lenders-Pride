from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.about, name="about"),
    path('',include('social_django.urls')),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]
