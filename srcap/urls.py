from django.urls import path
from .views import *

urlpatterns = [
    path('data/save/', DataSaveView.as_view(), name='home'),
    path('data/update/', DataUpdateView.as_view(), name='home'),
]