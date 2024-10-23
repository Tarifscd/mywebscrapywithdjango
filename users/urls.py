from django.urls import path
from .views import *


# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),




    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]