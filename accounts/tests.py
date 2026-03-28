from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import RegisterSerializer
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status



# Create your tests here.

class TestUserProfileModel(TestCase):

    def setUp(self):                     #is created temporary test data
        self.user = User.objects.create_user(
            username="revathy",
            password="test123"
        )

        self.profile = UserProfile.objects.create(
            user=self.user
        )

    def test_default_role_is_user(self):
        self.assertEqual(self.profile.role, "user")  #assertEqual checks whether actual output matches expected output.

    def test_str_method(self):
        self.assertEqual(str(self.profile),"revathy - user")    


class TestRegisterSerializer(TestCase):

    def setUp(self):

        self.valid_data = {    # self.valid_data = fake but correct registration input for testing.

            "username":"newuser",
            "email":"newuser@gmail.com",
            "password":"strongpass"
        }

    def test_serializer_is_valid_with_correct_data(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_creates_user(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, "newuser")

    def test_password_is_hashed(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertNotEqual(user.password, "strongpass")
        self.assertTrue(user.check_password("strongpass"))    


class TestRegisterAPIView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/register/"
        self.valid_data = {
            "username": "apiuser",
            "email": "apiuser@gmail.com",
            "password": "strongpass"
        }

    def test_register_api_success(self):
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestLoginAPIView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/login/"

        self.user = User.objects.create_user(
            username="loginuser",
            password="loginpass"
        )

        self.valid_data = {
            "username": "loginuser",
            "password": "loginpass"
        }
    

    class TestLoginAPIView(TestCase):

        def setUp(self):
            self.client = APIClient()
            self.url = "/api/accounts/login/"

            self.user = User.objects.create_user(
                username="loginuser",
                password="loginpass"
            )

            self.valid_data = {
                "username": "loginuser",
                "password": "loginpass"
            }

        def test_login_api_success(self):
            response = self.client.post(self.url, self.valid_data, format="json")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("access", response.data)

        def test_login_api_wrong_password(self):
            wrong_data = {
                "username": "loginuser",
                "password": "wrongpass"
            }
    
            response = self.client.post(self.url, wrong_data, format="json")
    
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    
