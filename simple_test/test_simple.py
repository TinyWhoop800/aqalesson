import pytest
import allure

class TestSimpleTest:
    @allure.title("Складываем 5 + 5")
    def test_a_plus_b(self):
        result = 5 + 5
        assert result == 10

# import requests
# import pytest
# from faker import Faker
#
# @pytest.fixture(scope='session')
# def base_url():
#     return 'http://localhost:8080'
#
# @pytest.fixture
# def faker_instance():
#     return Faker()
#
# @pytest.fixture
# def unique_user_data(faker_instance):
#     """Генерирует уникальные тестовые данные пользователя"""
#     return {
#         "username": faker_instance.user_name() + str(faker_instance.random_int(1000, 9999)),
#         "email": faker_instance.email(),
#         "password": faker_instance.password(length=12),
#     }
#
# def test_registration_with_fixtures(base_url, unique_user_data):
#     """Тест с использованием фикстур"""
#     url = f"{base_url}/api/auth/register"
#
#     response = requests.post(url, json=unique_user_data)
#
#     assert response.status_code == 200
#     data = response.json()
#     assert data["username"] == unique_user_data["username"]
#     assert data["email"] == unique_user_data["email"]
#
# @pytest.fixture
# def registered_user(base_url, unique_user_data):
#     """Фикстура для создания зарегистрированного пользователя"""
#     url = f"{base_url}/api/auth/register"
#     response = requests.post(url, json=unique_user_data)
#     user_data = response.json()
#
#     return {
#         "user_info": user_data,
#         "credentials": unique_user_data,
#     }
#
# def test_login_with_registered_user(base_url, registered_user):
#     """Тест логина с использованием фикстуры зарегестрированного пользователя"""
#     url = f"{base_url}/api/auth/login"
#     payload = {
#         "username":registered_user["credentials"]["username"],
#         "password": registered_user["credentials"]["password"],
#     }
#
#     response = requests.post(url, json=payload)
#
#     assert response.status_code == 200
#     data = response.json()
#     assert "token" in data