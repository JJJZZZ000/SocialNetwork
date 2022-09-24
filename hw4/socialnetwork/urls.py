from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.global_stream_action, name='home'),
    path('global_stream', views.global_stream_action, name='global_stream'),
    path('follower_stream', views.follower_stream_action, name='follower_stream'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('personal_profile', views.personal_profile_action, name='personal_profile'),
]