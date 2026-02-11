import requests

from src.main import TEST_USER, TEST_TASK

BASE_URL_GET = "https://postman-echo.com/get"
BASE_URL_POST = "https://postman-echo.com/post"


class TestPostmanApi:


    def test_get_basic(self):

        response = requests.get(BASE_URL_GET)

        assert response.status_code == 200
        data = response.json()

        assert "args" in data
        assert "headers" in data
        assert "url" in data
        assert data["url"] == BASE_URL_GET

    def test_get_with_query_params(self):

        params = {"username": "Nata", "email": "Nata@mail.com"}
        response = requests.get(BASE_URL_GET, params=params)

        assert response.status_code == 200
        data = response.json()
        assert data["args"] == params
        assert "username=Nata" in data["url"]
        assert 'email=Nata%40mail.com' in data["url"]



    def test_post_create_user(self):

        response = requests.post(BASE_URL_POST, json=TEST_USER)

        assert response.status_code == 200
        data = response.json()

        assert "json" in data
        assert data["json"] == TEST_USER
        assert data["url"] == BASE_URL_POST

    def test_post_create_task(self):

        response = requests.post(BASE_URL_POST, json=TEST_TASK)

        assert response.status_code == 200
        data = response.json()

        assert data["json"] == TEST_TASK

    def test_post_with_user_and_task(self):

        user_with_tasks = {
            "user": TEST_USER,
            "tasks": [TEST_TASK, {"title": "Good", "completed": True}]
        }

        response = requests.post(BASE_URL_POST, json=user_with_tasks)

        assert response.status_code == 200
        data = response.json()

        assert data["json"] == user_with_tasks



    def test_post_with_different_content_types(self):

        response = requests.post(
            BASE_URL_POST,
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        assert response.json()["headers"]["content-type"] == "application/json"


        response = requests.post(
            BASE_URL_POST,
            data=TEST_USER,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "form" in data
        assert data["form"]["username"] == "Nata"
        assert data["form"]["email"] == "Nata@mail.com"




    def test_get_with_negative_data(self):

        response = requests.get(
        BASE_URL_GET,
        params={"endpoint": "users/nonexistent-id"}
    )

        assert response.status_code == 400
        data = response.json()

        assert data["args"]["endpoint"] == "users/nonexistent-id"




