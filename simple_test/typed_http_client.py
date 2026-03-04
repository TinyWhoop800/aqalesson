# import pytest
# from pydantic import BaseModel
# from faker import Faker
#
# from simple_test.simple_http_client import SimpleHttpClient
#
#
# class RegisterRequest(BaseModel):
#     username: str
#     email: str
#     password: str
#
# class UserResponseDto(BaseModel):
#     id: int
#     username: str
#     email: str
#     role: str
#
# class AuthRequest(BaseModel):
#     username: str
#     password: str
#
#
# class AuthResponse(BaseModel):
#     token: str
#     user: UserResponseDto
#
# class TypedHttpClient(SimpleHttpClient):
#     """HTTP клиент с поддержкой Pydantic моделей"""
#     def post_typed(self, path: str, request_model: BaseModel = None, response_model: type = None):
#         """POST запрос с типизацией"""
#         data = request_model.model_dump() if request_model else None
#         response_data = self.post(path, data)
#
#         if response_model and response_data:
#             return response_model.model_validate(response_data)
#         return response_data
#
# @pytest.fixture(scope="session")
# def base_url():
#     return "http://localhost:8080"
#
# @pytest.fixture
# def faker_instance():
#     return Faker()
#
# @pytest.fixture
# def typed_user_data(faker_instance):
#     """Генерирует уникальные тестовые данные пользователя"""
#     return RegisterRequest(
#         username = faker_instance.user_name() + str(faker_instance.random_int(1000, 9999)),
#         email = faker_instance.email(),
#         password = faker_instance.password(length=12),
#     )
#
# @pytest.fixture(scope="session")
# def typed_api_client(base_url):
#     return TypedHttpClient(base_url=base_url)
#
# def test_with_typed_model(typed_api_client, typed_user_data):
#     # Регистрация с типизацией
#     user_response = typed_api_client.post_typed(
#         path="/api/auth/register",
#         request_model=typed_user_data,
#         response_model=UserResponseDto
#     )
#
#     assert user_response.username == typed_user_data.username
#     assert user_response.email == typed_user_data.email
#
#     # Логин с типизацией
#     auth_request = AuthRequest(
#         username = typed_user_data.username,
#         password = typed_user_data.password,
#     )
#
#     auth_response = typed_api_client.post_typed(
#         "/api/auth/login",
#         request_model=auth_request,
#         response_model=AuthResponse
#     )
#
#     assert auth_response.token is not None
#     assert auth_response.user.username == typed_user_data.username