from django.contrib.auth import get_user_model
from django.test import TestCase

from users.serializers import UserPersonalInfoDetailSerializer, \
    UserDetailSerializer, UserLoginSerializer, ShortUserInfoSerializer

User = get_user_model()


class TestLoginSerializer(TestCase):
    """Сериалайзер логина. Вход по username и password"""
    def test_login_required_date(self):
        """ Заполнена только основная информация"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com'
        }
        user = User(**user_data)
        user.set_password('StrongPassword123')
        user.save()
        data = UserLoginSerializer(user).data
        expected_data = {'username': 'test_user', 'password': user.password}
        self.assertEqual(expected_data, data)


class UserPersonalInfoDetailSerializerTestCase(TestCase):
    """Тест сериалайзера персональной информации
    для отображения в профиле пользователя."""

    def test_personal_info_filled_only_main_data(self):
        """ Заполнена только основная информация"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com'
        }
        user = User.objects.create(**user_data)
        data = UserPersonalInfoDetailSerializer(user).data
        expected_data = {
            'id': user.id,
            'username': 'test_user',
            'name': 'test_user',
            'avatar': None,  # fix, should return default picture
            'header': None,  # fix, should return default picture
            'description': None,
            'location': None,
            'site': None
        }
        self.assertEqual(expected_data, data)

    def test_personal_info_all_data(self):
        """Заполнены все данные"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com',
            'avatar': '/uploads/avatar/test.jpg',
            'header': '/uploads/header/test.jpg',
            'description': 'Test user description',
            'location': 'Test place location',
            'site': 'https://test-site.com'
        }

        user = User.objects.create(**user_data)
        data = UserPersonalInfoDetailSerializer(user).data
        expected_data = {
            'id': user.id,
            'username': 'test_user',
            'name': 'test_user',
            'avatar': '/media/uploads/avatar/test.jpg',
            'header': '/media/uploads/header/test.jpg',
            'description': 'Test user description',
            'location': 'Test place location',
            'site': 'https://test-site.com'
        }
        self.assertEqual(expected_data, data)


class ShortUserInfoSerializerTestCase(TestCase):
    """
    Тест сериалайзера краткой информауии о пользователе
    """

    def test_short_user_info_filled_only_main_data(self):
        """ Заполнена только основная информация"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com'
        }
        user = User.objects.create(**user_data)
        data = ShortUserInfoSerializer(user).data
        expected_data = {
            'id': user.id,
            'username': 'test_user',
            'name': 'test_user',
            'avatar': None,  # fix, should return default picture
        }
        print(expected_data)
        print(data)
        self.assertEqual(expected_data, data)

    def test_short_user_info_all_data(self):
        """Заполнены все данные"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com',
            'avatar': '/uploads/avatar/test.jpg',
            'header': '/uploads/header/test.jpg',
            'description': 'Test user description',
            'location': 'Test place location',
            'site': 'https://test-site.com'
        }

        user = User.objects.create(**user_data)
        data = ShortUserInfoSerializer(user).data
        expected_data = {
            'id': user.id,
            'username': 'test_user',
            'name': 'test_user',
            'avatar': '/media/uploads/avatar/test.jpg',
        }
        print(expected_data)
        print(data)
        self.assertEqual(expected_data, data)


class UserDetailSerializerTestCase(TestCase):
    """Тест сериалайзера личных данных пользователя"""

    def test_user_detail_filled_only_main_data(self):
        """ Заполнена только основная информация"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com'
        }
        user = User.objects.create(**user_data)
        data = UserDetailSerializer(user).data
        expected_data = {
            'id': user.id,
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com',
            'first_name': None,
            'last_name': None,
            'phone_number': None,
            'date_of_birth': None,
            'gender': None,
            'country': None
        }
        self.assertEqual(expected_data, data)

    def test_user_detail_filled_all_the_data(self):
        """ Заполнена вся информация"""
        user_data = {
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com',
            'first_name': 'Test',
            'last_name': 'Testovich',
            'phone_number': '79998880066',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'country': 'RU',
            'description': 'Some test information',
            'location': 'Test place',
        }
        user = User.objects.create(**user_data)
        data = UserDetailSerializer(user).data
        expected_data = {
            'id': user.id,
            'username': 'test_user',
            'name': 'test_user',
            'email': 'test_user@gmail.com',
            'first_name': 'Test',
            'last_name': 'Testovich',
            'phone_number': '79998880066',
            'date_of_birth': '1990-01-01',
            'gender': 'male',
            'country': 'RU'
        }
        self.assertEqual(expected_data, data)
