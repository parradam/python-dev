from fastapi import status
from fastapi.testclient import TestClient


def test_create_resource_returns_201_with_valid_data(client: TestClient) -> None:
    resource = {
        "name": "thename",
        "link": "thelink",
        "isbn": "theisbn",
    }

    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response_json["name"] == resource["name"]
    assert response_json["link"] == resource["link"]
    assert response_json["isbn"] == resource["isbn"]


def test_create_resource_returns_201_without_optional_fields(client: TestClient) -> None:
    resource = {
        "name": "thename",
    }

    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response_json
    assert response_json["name"] == resource["name"]


def test_create_resource_returns_422_without_name(client: TestClient) -> None:
    resource = {
        "link": "thelink",
        "isbn": "theisbn",
    }

    response = client.post(
        "/resources/",
        json=resource,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_resources_returns_200_with_list(client: TestClient) -> None:
    resource = {
        "name": "thename",
        "link": "thelink",
        "isbn": "theisbn",
    }
    client.post(
        "/resources/",
        json=resource,
    )

    read_response = client.get("/resources/")
    read_response_json = read_response.json()

    assert read_response.status_code == status.HTTP_200_OK
    assert "id" in read_response_json[0]
    assert read_response_json[0]["name"] == resource["name"]
    assert read_response_json[0]["link"] == resource["link"]
    assert read_response_json[0]["isbn"] == resource["isbn"]


def test_update_resource_returns_200_with_data(client: TestClient) -> None:
    resource = {
        "name": "original_name",
        "link": "original_link",
        "isbn": "original_isbn",
    }
    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    updated_resource = {
        "name": "updated_name",
        "link": "updated_link",
        "isbn": "updated_isbn",
    }
    updated_response = client.put(
        f"/resources/{response_json['id']}",
        json=updated_resource,
    )
    updated_response_json = updated_response.json()

    assert updated_response.status_code == status.HTTP_200_OK
    assert "id" in updated_response_json
    assert updated_response_json["name"] == updated_resource["name"]
    assert updated_response_json["link"] == updated_resource["link"]
    assert updated_response_json["isbn"] == updated_resource["isbn"]


def test_update_resource_returns_200_without_optional_data(client: TestClient) -> None:
    resource = {
        "name": "original_name",
        "link": "original_link",
        "isbn": "original_isbn",
    }
    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    updated_resource = {
        "name": "updated_name_only",
    }
    updated_response = client.put(
        f"/resources/{response_json['id']}",
        json=updated_resource,
    )
    updated_response_json = updated_response.json()

    assert updated_response.status_code == status.HTTP_200_OK
    assert "id" in updated_response_json
    assert updated_response_json["name"] == updated_resource["name"]
    assert updated_response_json["link"] == resource["link"]
    assert updated_response_json["isbn"] == resource["isbn"]


def test_update_resource_returns_200_with_unset_data(client: TestClient) -> None:
    resource = {
        "name": "original_name",
        "link": "original_link",
        "isbn": "original_isbn",
    }
    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    # name isn't provided, so shouldn't be updated
    updated_resource = {
        "link": "updated_link",
        "isbn": "updated_isbn",
    }
    updated_response = client.put(
        f"/resources/{response_json['id']}",
        json=updated_resource,
    )

    assert updated_response.status_code == status.HTTP_200_OK


def test_update_resource_returns_422_with_invalid_data(client: TestClient) -> None:
    resource = {
        "name": "original_name",
        "link": "original_link",
        "isbn": "original_isbn",
    }
    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    # name is provided, so should cause a validation error (too short)
    updated_resource = {
        "name": "a",
    }
    updated_response = client.put(
        f"/resources/{response_json['id']}",
        json=updated_resource,
    )

    assert updated_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_resource_returns_204_when_id_exists(client: TestClient) -> None:
    resource = {
        "name": "original_name",
        "link": "original_link",
        "isbn": "original_isbn",
    }
    response = client.post(
        "/resources/",
        json=resource,
    )
    response_json = response.json()

    deleted_response = client.delete(
        f"/resources/{response_json['id']}",
    )

    assert deleted_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_resource_returns_204_when_id_does_not_exist(client: TestClient) -> None:
    deleted_response = client.delete(
        "/resources/99999999999999",
    )

    assert deleted_response.status_code == status.HTTP_204_NO_CONTENT
