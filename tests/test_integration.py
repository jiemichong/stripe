import json
import pytest


def call(client, path, method='GET', body=None):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    if method == 'POST':
        response = client.post(path, data=json.dumps(body), headers=headers)
        print(response.data.decode('utf-8'))
        print(response.status_code)
    elif method == 'PUT':
        response = client.put(path, data=json.dumps(body), headers=headers)
    elif method == 'PATCH':
        response = client.patch(path, data=json.dumps(body), headers=headers)
    elif method == 'DELETE':
        response = client.delete(path)
    else:
        response = client.get(path)

    return {
        "code": response.status_code
    }


@pytest.mark.dependency()
def test_health(client):
    result = call(client, 'health')
    assert result['code'] == 200


@pytest.mark.dependency()
def test_room_1(client):
    result = call(client, 'create-checkout-session/1/1', 'GET')
    assert result['code'] == 303


@pytest.mark.dependency()
def test_room_2(client):
    result = call(client, 'create-checkout-session/2/1', 'GET')
    assert result['code'] == 303


@pytest.mark.dependency()
def test_room_3(client):
    result = call(client, 'create-checkout-session/3/1', 'GET')
    assert result['code'] == 303


@pytest.mark.dependency()
def test_room_4(client):
    result = call(client, 'create-checkout-session/4/1', 'GET')
    assert result['code'] == 303


@pytest.mark.dependency()
def test_room_5(client):
    result = call(client, 'create-checkout-session/5/1', 'GET')
    assert result['code'] == 303
