import imp
from webbrowser import get
from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('category/<int:category_id>/', get_category),
]