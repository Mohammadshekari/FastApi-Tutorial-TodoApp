def test_root_response_404(anon_client):
    response = anon_client.get('/')
    assert response.status_code == 404


def test_login_response_401(anon_client):
    payload = {
        'username': 'mohammad',
        'password': '1234',
    }
    response = anon_client.post('/api/v1/user/login', json=payload)
    assert response.status_code == 401


def test_register_response_201(anon_client):
    payload = {
        'username': 'mohammad',
        'password': '1234',
        'password_confirm': '1234',
    }
    response = anon_client.post('/api/v1/user/register', json=payload)
    assert response.status_code == 201
