# import allure
# from allure_commons.types import AttachmentType
# from pydantic import BaseModel
# import json
#
# from simple_test.typed_http_client import TypedHttpClient
#
#
#
# class AllureHttpClient(TypedHttpClient):
#     """HTTP клиент с интеграцией Allure"""
#     def post_typed(self, path: str, request_model: BaseModel = None, response_model: type = None, step_title: str = None):
#         """POST запрос с Allure шагами"""
#         title = step_title or f"POST {path}"
#
#         with allure.step(title):
#             # Аттачим запрос
#             if request_model:
#                 request_json = json.dumps(request_model.model_dump(), indent=2, ensure_ascii=False)
#                 allure.attach(request_json, name="Request Body", attachment_type=AttachmentType.JSON)
#
#             # Выполняем запрос
#             data = request_model.model_dump() if request_model else None
#             response_data = self.post(path, data)
#
#             # Аттачим ответ
#             if response_data:
#                 response_json = json.dumps(response_data, indent=2, ensure_ascii=False)
#                 allure.attach(response_json, name="Response Body", attachment_type=AttachmentType.JSON)
#
#             # Возвращаем типизированный результат
#             if response_model and response_data:
#                 return response_model.model_validate(response_data)
#             return response_data