from django.urls import path
from .views import UserRegisterView,VerifyMailView,UserLoginView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('mail-verify/', VerifyMailView.as_view(), name="mail-verify"),
    path('login/', UserLoginView.as_view(), name="login"),
]