from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    ListPrescriptionsAPIView,
    DeletePrescriptionsAPIView,
    CreatePrescriptionsAPIView,
    UpdatePrescriptionsAPIView
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('list',ListPrescriptionsAPIView.as_view(),name="prescription_list"),
    path('create/',CreatePrescriptionsAPIView.as_view(),name="prescription_create"),
    path('update/<int:pk>',UpdatePrescriptionsAPIView.as_view(),name="prescription_update"),
    path('delete/<int:pk>',DeletePrescriptionsAPIView.as_view(),name="prescription_delete")
]