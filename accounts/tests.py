from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

PASSWORD = 'Str0ng-Passw0rd!'


class UserModelTests(TestCase):
    def test_custom_user_model_is_active(self):
        self.assertEqual(User._meta.label, 'accounts.User')
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertNotIn('username', [f.name for f in User._meta.get_fields()])

    def test_create_user(self):
        user = User.objects.create_user(email='anna@example.com', first_name='Anna', password=PASSWORD)

        self.assertEqual(user.email, 'anna@example.com')
        self.assertEqual(user.first_name, 'Anna')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), 'anna@example.com')

    def test_password_is_hashed(self):
        user = User.objects.create_user(email='anna@example.com', first_name='Anna', password=PASSWORD)
        user.refresh_from_db()

        self.assertNotEqual(user.password, PASSWORD)
        self.assertNotIn(PASSWORD, user.password)
        self.assertTrue(user.password.startswith(('pbkdf2_sha256$', 'argon2', 'bcrypt', 'scrypt')))
        self.assertTrue(user.check_password(PASSWORD))

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', first_name='Anna', password=PASSWORD)

    def test_email_is_normalized_to_lowercase(self):
        user = User.objects.create_user(email='  Anna@Example.COM ', first_name='Anna', password=PASSWORD)

        self.assertEqual(user.email, 'anna@example.com')

    def test_email_must_be_unique(self):
        User.objects.create_user(email='anna@example.com', first_name='Anna', password=PASSWORD)

        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create_user(email='anna@example.com', first_name='Other', password=PASSWORD)

    def test_email_uniqueness_is_case_insensitive(self):
        User.objects.create_user(email='anna@example.com', first_name='Anna', password=PASSWORD)

        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create_user(email='ANNA@example.com', first_name='Other', password=PASSWORD)

    def test_first_name_is_required(self):
        user = User(email='anna@example.com', first_name='')
        user.set_password(PASSWORD)

        with self.assertRaises(ValidationError) as ctx:
            user.full_clean()
        self.assertIn('first_name', ctx.exception.message_dict)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(email='admin@example.com', first_name='Admin', password=PASSWORD)

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_rejects_non_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', first_name='Admin', password=PASSWORD, is_staff=False
            )

    def test_user_can_authenticate_with_email_and_password(self):
        User.objects.create_user(email='anna@example.com', first_name='Anna', password=PASSWORD)

        self.assertIsNotNone(authenticate(username='anna@example.com', password=PASSWORD))
        self.assertIsNone(authenticate(username='anna@example.com', password='wrong-password'))


class UserAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@example.com', first_name='Admin', password=PASSWORD)
        self.client.force_login(self.admin)

    def test_changelist_and_change_pages_load(self):
        self.assertEqual(self.client.get(reverse('admin:accounts_user_changelist')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('admin:accounts_user_change', args=[self.admin.pk])).status_code, 200
        )

    def test_admin_can_add_user(self):
        response = self.client.post(
            reverse('admin:accounts_user_add'),
            {
                'email': 'Jan@Example.com',
                'first_name': 'Jan',
                'password1': PASSWORD,
                'password2': PASSWORD,
                'usable_password': 'true',
            },
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='jan@example.com')
        self.assertTrue(user.check_password(PASSWORD))
