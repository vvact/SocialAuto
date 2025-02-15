from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-reset/', reset_password_request_token, name='password_reset_request'),
    path('password-reset/confirm/', reset_password_confirm, name='password_reset_confirm'),

    # ✅ Add JWT Token Routes
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
