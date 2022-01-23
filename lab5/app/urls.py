from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scraping/',views.scraping, name = "scraping"),
    path('xpath/', views.xml, name= "xpath"),
]