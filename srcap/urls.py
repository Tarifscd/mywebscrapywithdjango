from django.urls import path
from .views import *

urlpatterns = [
    path('data/', DataSaveView.as_view(), name='home'),  # This maps the home view to the root URL of the app.
]