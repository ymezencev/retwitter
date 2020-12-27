import json

from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory
from datetime import date
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.serializers import UserPersonalInfoDetailSerializer, \
    UserDetailSerializer

User = get_user_model()
REGISTER_DATA = {
    'username': 'test_user',
    'email': 'test_user@email.ru',
    'password1': 'secretStrongPass123',
    'password2': 'secretStrongPass123',
}
LOGIN_DATA = {
    'username': REGISTER_DATA['username'],
    'password': REGISTER_DATA['password1'],
}
REGISTER_URL = reverse('rest_register')
LOGIN_URL = reverse('rest_login')
LOGOUT_URL = reverse('rest_logout')
USER_URL = reverse('rest_user_details')


class UserAuthRegisterTestCase(APITestCase):
    """Тесты регистрации пользователя"""
    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        """Тест успешной регистрации"""
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(REGISTER_DATA['username'],
                         response.data['user']['username'])
        self.assertEqual(REGISTER_DATA['email'],
                         response.data['user']['email'])

    def test_register_failure_not_unique_username(self):
        """Регистрация не успешна, username должно быть уникальным"""
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        test_user2_data = REGISTER_DATA.copy()
        test_user2_data['username'] = 'test_user2'
        response = self.client.post(REGISTER_URL, test_user2_data)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('A user is already registered with this e-mail '
                        'address.' in response.data['email'])

    def test_register_failure_not_unique_email(self):
        """Регистрация не успешна, email должен быть уникальным"""
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        test_user2_data = REGISTER_DATA.copy()
        test_user2_data['email'] = 'test_user2@email.ru'
        response = self.client.post(REGISTER_URL, test_user2_data)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('User with this username already exists.' in
                        response.data['username'])

    def test_register_failure_user_exists(self):
        """Регистрация не успешна, пользователь существует"""
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('User with this username already exists.' in
                        response.data['username'])

    def test_register_failure_passwords_dont_match(self):
        """Регистрация не успешна, пароли не совпадают"""
        test_user_data = REGISTER_DATA.copy()
        test_user_data['password2'] = 'different_password'
        response = self.client.post(REGISTER_URL, test_user_data)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('The two password fields didn\'t match.' in
                        response.data['non_field_errors'])

    def test_register_success_name_equals_username_when_first_create(self):
        """При создании имя пользователя должно совпадать с логином
        name = username"""
        response = self.client.post(REGISTER_URL, REGISTER_DATA)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        user = User.objects.get(username=REGISTER_DATA['username'])
        self.assertEqual(user.name, response.data['user']['username'])


class UserAuthLoginTestCase(APITestCase):
    """Тесты авторизации пользователя"""
    def setUp(self):
        self.client = Client()
        self.client.post(REGISTER_URL, REGISTER_DATA)

    def test_login_success(self):
        """Тест успешной авторизауии"""
        response = self.client.post(LOGIN_URL, LOGIN_DATA)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(LOGIN_DATA['username'],
                         response.data['user']['username'])

    def test_login_failure_incorrect_password(self):
        """Авторизация не успешна, неправильный пароль"""
        test_user_data = LOGIN_DATA.copy()
        test_user_data['password'] = 'incorrect_password'
        response = self.client.post(LOGIN_URL, test_user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('Unable to log in with provided credentials.' in
                        response.data['non_field_errors'])

    def test_login_failure_user_not_exist(self):
        """Авторизация не успешна, пользователь не существует"""
        test_user_data = {'username': 'non_existent_user',
                          'password': 'incorrect_password'}
        response = self.client.post(LOGIN_URL, test_user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('Unable to log in with provided credentials.' in
                        response.data['non_field_errors'])


class UserEditTestCase(APITestCase):
    """Тесты редактирования личных данных пользователя"""

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': REGISTER_DATA['username'],
            'name': REGISTER_DATA['username'],
            'email': REGISTER_DATA['email'],
            'first_name': 'Test',
            'last_name': 'Testovich',
            'phone_number': '79778889900',
            'date_of_birth': str(date(year=1990, month=1, day=10)),
            'gender': 'male',
            'country': 'RU'
        }
        self.user = User(**self.user_data)
        self.user.set_password(REGISTER_DATA['password1'])
        self.user.save()
        self.client.post(LOGIN_URL, data=LOGIN_DATA)

        context = {'request': RequestFactory().get('/')}
        self.user_info = UserDetailSerializer(self.user, context=context).data

    def test_get_success_user_data_for_edit(self):
        """Успешное получение данных пользователя для редактирования"""
        response = self.client.get(USER_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user_info, response.data)

    def test_get_failure_user_data_for_edit_not_logged_in(self):
        """Ошибка получения данных пользователя для редактирования
        пользователь не авторизован"""
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(USER_URL)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertTrue('Authentication credentials were not provided.' in
                        response.data['detail'])

    def test_patch_success_user_data_for_edit(self):
        """Успешное обновление данных пользователя"""
        fields_for_edit = {'username': 'new_test_user_username'}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(USER_URL, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_info['username'] = fields_for_edit['username']
        self.assertEqual(self.user_info, response.data)

    def test_patch_success_user_data_for_edit_not_logged_in(self):
        """Ошибка обновления данных пользователя,
        пользователь не авторизован"""
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        fields_for_edit = {'username': 'new_test_user_username'}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(USER_URL, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertTrue('Authentication credentials were not provided.' in
                        response.data['detail'])

    def test_patch_failure_user_data_for_edit_required_fields_empty(self):
        """Ошибка обновления данных пользователя,
        переданы не все необходимые данные"""
        fields_for_edit = {'username': '', 'name': '', 'email': ''}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(USER_URL, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('This field may not be blank.' in
                        response.data['username'])
        self.assertTrue('This field may not be blank.' in
                        response.data['name'])
        self.assertTrue('This field may not be blank.' in
                        response.data['email'])

    def test_patch_failure_user_data_for_edit_new_username_exist(self):
        """Ошибка обновления данных пользователя, username уже занято"""
        user_test2_data = REGISTER_DATA.copy()
        user_test2_data['username'] = 'for_duplicate_username_test'
        user_test2_data['email'] = 'user_test2@gmail.com'
        response = self.client.post(REGISTER_URL, user_test2_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        fields_for_edit = {'username': REGISTER_DATA['username']}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(USER_URL, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('user with this username already exists.' in
                        response.data['username'])

    def test_patch_failure_user_data_for_edit_new_email_exist(self):
        """Ошибка обновления данных пользователя, email уже занят"""
        user_test2_data = REGISTER_DATA.copy()
        user_test2_data['username'] = 'user_test2'
        user_test2_data['email'] = 'for_duplicate_username_test@gmail.com'
        response = self.client.post(REGISTER_URL, user_test2_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        fields_for_edit = {'email': REGISTER_DATA['email']}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(USER_URL, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('user with this email already exists.' in
                        response.data['email'])


class UserPersonalInfoDetailTestCase(APITestCase):
    """Тесты редактирования персональной информации пользователя"""

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': REGISTER_DATA['username'],
            'name': REGISTER_DATA['username'],
            'email': REGISTER_DATA['email'],
            'avatar': '/uploads/avatar/test.jpg',
            'header': '/uploads/header/test.jpg',
            'description': 'Test user description',
            'location': 'Test place location',
            'site': 'https://test-site.com'
        }
        self.user = User(**self.user_data)
        self.user.set_password(REGISTER_DATA['password1'])
        self.user.save()
        context = {'request': RequestFactory().get('/')}
        self.personal_info = UserPersonalInfoDetailSerializer(
            self.user, context=context).data
        self.client.post(LOGIN_URL, data=LOGIN_DATA)
        self.personal_info_url = reverse('user-info-detail',
                                         args=(self.user.id,))

    def test_get_success_personal_info_for_edit(self):
        """Успешное получение данных пользователя для редактирования"""
        response = self.client.get(self.personal_info_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.personal_info, response.data)

    def test_get_failure_personal_info_for_edit_not_logged_in(self):
        """Ошибка получения данных пользователя для редактирования
        пользователь не авторизован"""
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(self.personal_info_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertTrue('Authentication credentials were not provided.' in
                        response.data['detail'])

    def test_patch_success_personal_info_for_edit(self):
        """Успешное обновление данных пользователя"""
        fields_for_edit = {'description': 'New test user description'}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(self.personal_info_url, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.personal_info['description'] = fields_for_edit['description']
        self.assertEqual(self.personal_info, response.data)

    def test_patch_failure_personal_info_username_name_not_changed(self):
        """Успешное обновление данных пользователя"""
        fields_for_edit = {'username': 'new_test_user_username',
                           'name': 'new_test_user_name'}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(self.personal_info_url, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.username, response.data['username'])

    def test_patch_success_personal_info_for_edit_not_logged_in(self):
        """Ошибка обновления данных пользователя,
        пользователь не авторизован"""
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        fields_for_edit = {'username': 'new_test_user_username'}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(self.personal_info_url, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertTrue('Authentication credentials were not provided.' in
                        response.data['detail'])

    def test_patch_failure_personal_info_for_edit(self):
        """Ошибка при попытке обновить не доступные для обновления данные"""
        fields_for_edit = {'email': 'new_test_user_email@gmail.com'}
        json_data = json.dumps(fields_for_edit)
        response = self.client.patch(self.personal_info_url, json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user = User.objects.get(id=self.user.id)
        self.assertEquals(self.user.email, user.email)
