from django.test import TestCase
from django.contrib.auth import get_user_model

from user.services import UserService

User = get_user_model()

class UserServiceTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "test_password"
        self.telegram_id = 123456789
        self.last_name = "Test"
        self.language_code = "en"

    def test_create_user(self):
        user = UserService.create_user(
            username=self.username,
            password=self.password,
            telegram_id=self.telegram_id,
            last_name=self.last_name,
            language_code=self.language_code
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.telegram_id, self.telegram_id)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.language_code, self.language_code)
        self.assertTrue(user.check_password(self.password))

    def test_get_or_create_user_by_telegram_id_existing_user(self):
        UserService.create_user(
            username=self.username,
            password=self.password,
            telegram_id=self.telegram_id
        )
        user = UserService.get_or_create_user_by_telegram_id(
            telegram_id=self.telegram_id,
            username=self.username,
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.telegram_id, self.telegram_id)
        self.assertEqual(user.username, self.username)

    def test_get_or_create_user_by_telegram_id_new_user(self):
        new_telegram_id = 987654321
        new_username = "newuser"
        new_password = "new_test_password"
        user = UserService.get_or_create_user_by_telegram_id(
            telegram_id=new_telegram_id,
            username=new_username,
            password=new_password
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.telegram_id, new_telegram_id)
        self.assertEqual(user.username, new_username)
        self.assertTrue(user.check_password(new_password))
