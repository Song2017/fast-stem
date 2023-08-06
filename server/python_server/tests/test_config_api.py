# coding: utf-8

from fastapi.testclient import TestClient


from http_server.models.api_response import ApiResponse  # noqa: F401


def test_get_config(client: TestClient):
    """Test case for get_config

    GetConfig
    """
    params = [("connector", 'connector_example'),     ("cache", 'cache_example')]
    headers = {
        "ca_key": "special-key",
    }
    response = client.request(
        "GET",
        "/config/connector/{id}".format(id='id_example'),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

