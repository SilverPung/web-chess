from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
]