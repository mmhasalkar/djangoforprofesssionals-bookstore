from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase


class CustomUserTests(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@email.com',
            password='testadminpass123'
        )

        self.assertEqual(admin_user.username, 'testadmin')
        self.assertEqual(admin_user.email, 'testadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupPageTests(TestCase):

    username = 'newuser'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hey, There! I should not be on the page.')

    def test_signup_form(self):
        # Older test code - when signup was a custom page
        # form = self.response.context.get('form')
        # self.assertIsInstance(form, CustomUserCreationForm)
        # self.assertContains(self.response, 'csrfmiddlewaretoken')

        # New test code - when signup is being used from django-allauth
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)

    # Commenting this test as now django-allauth being used for signup
    # def test_signup_view(self):
    #     view = resolve('/accounts/signup/')
    #     self.assertEqual(view.func.__name__, SignupPageView.as_view().__name__)
