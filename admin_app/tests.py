from django.test import TestCase
from django.contrib.auth.models import User
from .models import AdminProfile

# Create your tests here.


class  TestAdminProfileModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username= "adminuser",
            password= "test123" 
        )

        self.profile = AdminProfile.objects.create(
            user = self.user,
            image= "base64imagestring"
        )

    def test_admin_profile_user_link(self):
        self.assertEqual(self.profile.user.username,"adminuser")

