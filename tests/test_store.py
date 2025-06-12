import allure
import pytest
import requests
import jsonschema

from .conftest import order_placing
from .schemas.store_schema import STORE_SCHEMA
from tests.test_pet import BASE_URL


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа ")
    def test_order_placing(self):
        with allure.step("Подготовка данных для отправки запроса на размещение заказа"):
            payload = {
                 "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидации json схемы"):
            response.status_code == 200
            jsonschema.validate(response.json(), STORE_SCHEMA)

        with allure.step("Проверка получения корректных данных заказа"):
            assert response_json["id"] == payload["id"], "ID не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "petId не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "quantity не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], "complete не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_info_about_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о заказе по id"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            store_id = response.json()["id"]

        with allure.step("Проверка получения статус-кода информации о заказе по id"):
            assert response.status_code == 200
            assert response.json()["id"] == store_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, order_placing):
        with allure.step("Получение ID заказа"):
            order_id = order_placing["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200

        with allure.step("Отправка запроса на получение удаленного заказа по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_info_about_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе и проверка статус-кода"):
            response = requests.get(f"{BASE_URL}/store/order/9999")
            assert response.status_code == 404


