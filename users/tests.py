from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthenticationTests(APITestCase):

    def setUp(self):
        """Set up a user for testing"""
        self.user = User.objects.create_user(email="testuser@example.com", password="Test@1234")
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.logout_url = "/api/auth/logout/"
        self.password_reset_url = "/api/auth/password-reset/"
        self.password_reset_confirm_url = "/api/auth/password-reset/confirm/"

    def test_user_registration(self):
        """Test if a user can register successfully"""
        data = {
            "email": "newuser@example.com",
            "password": "NewPassword@123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully")

    def test_user_login(self):
        """Test if a user can log in and receive an access and refresh token"""
        data = {
            "email": "testuser@example.com",
            "password": "Test@1234"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_logout(self):
        """Test if a user can log out successfully"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        data = {"refresh": str(refresh)}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")

    def test_password_reset_request(self):
        """Test if a password reset request can be made"""
        data = {"email": "testuser@example.com"}
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset link sent to your email")

    def test_password_reset_confirm(self):
        """Simulate password reset confirmation"""
        token = "dummy-token"  # Replace with an actual token during real tests
        data = {
            "token": token,
            "new_password": "NewSecurePassword@123"
        }
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password reset successful")

