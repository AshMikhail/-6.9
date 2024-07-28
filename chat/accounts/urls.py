from django.contrib.auth import views as a_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('AllUsers/', views.AllUsers, name="AllUsers"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile, name='profile_edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', a_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
