from django.urls import path
from . import views

urlpatterns = [
    path('', views.chop_url, name='chop_url'),
    path('<str:code>/', views.redirect_url, name='redirect_url'),
]