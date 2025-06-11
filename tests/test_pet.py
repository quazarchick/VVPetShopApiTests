import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновления несуществующего питомца")
    def test_put_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }

            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получения информации о несуществующем питомце")
    def test_get_nonexistence_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на добавление нового питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title('Добавление нового питомца c полными данными')
    def test_add_full_data_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = { "id": 10,
                        "name": "doggie",
                        "category": {
                            "id": 1,
                            "name": "Dogs"
                        },
                        "photoUrls": ["string"],
                        "tags": [{
                            "id": 0,
                            "name": "string"}],
                        "status": "available"
                        }
        with allure.step("Отправка запроса на добавление нового питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Name питомца не совпадает с ожидаемым"
            assert response_json['category']['id'] == payload['category']['id'], "Категория питомца (id) не совпадает с ожидаемым"
            assert response_json['category']['name'] == payload['category']['name'], "Категория питомца (name) не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls не совпадает с ожидаемым"
            assert response_json['tags'][0]['id'] == payload['tags'][0]['id'], 'tags id не совпадает с ожидаемым'
            assert response_json['tags'][0]['name'] == payload['tags'][0]['name'], 'tags name не совпадает с ожидаемым'
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_info_by_id(self, create_pet):
        with allure.step("Получение ID питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка на получение информации о питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_info_about_pet(self, create_pet):
        with allure.step("Получение ID питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка информации на обновление информации о питомце"):
            payload = {
                        "id": pet_id,
                        "name": "Buddy Updated",
                        "status": "sold"
                    }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            assert response.status_code == 200
            assert response.json()["id"] == pet_id
            assert response.json()["name"] == payload["name"]
            assert response.json()["status"] == payload["status"]

    @allure.title("Удаление питомца по ID")
    def test_delete_info_about_pet(self, create_pet):
        with allure.step("Получение питомца по ID"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200

        with allure.step("Проверка удаления питомца через GET запрос"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status", "expected_status_code",
        [
            ("availble", 200),
            ("pending", 200),
            ("sold", 200),
            ("unbelieve", 200),
            ("", 200)
        ]
    )
    def get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомца по статусуP{status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), list)