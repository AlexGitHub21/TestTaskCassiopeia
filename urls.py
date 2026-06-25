from django.urls import path
from . import views

urlpatterns = [
    path('feed_yml', views.yml_feed, name='feed_yml'),
]