import pytest

def test_register_success(client):
    """
    Test: Registro de usuario exitoso
    """
    response = client.post('/api/auth/register', json={
        'email': 'newuser@test.com',
        'password': 'password123',
        'first_name': 'New',
        'last_name': 'User',
        'role': 'client'
    })
    
    assert response.status_code == 201
    assert response.json['message'] == 'Usuario registrado exitosamente'
    assert response.json['user']['email'] == 'newuser@test.com'

def test_register_missing_fields(client):
    """
    Test: Registro sin campos requeridos debe fallar
    """
    response = client.post('/api/auth/register', json={
        'email': 'incomplete@test.com',
        'password': 'password123'
        # Faltan first_name y last_name
    })
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_register_duplicate_email(client, client_user):
    """
    Test: Registro con email duplicado debe fallar
    """
    response = client.post('/api/auth/register', json={
        'email': 'client@test.com',  # Email ya existe
        'password': 'password123',
        'first_name': 'Duplicate',
        'last_name': 'User'
    })
    
    assert response.status_code == 409
    assert 'error' in response.json

def test_login_success(client, client_user):
    """
    Test: Login exitoso con credenciales correctas
    """
    response = client.post('/api/auth/login', json={
        'email': 'client@test.com',
        'password': 'client123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert response.json['user']['email'] == 'client@test.com'

def test_login_wrong_password(client, client_user):
    """
    Test: Login con contraseña incorrecta debe fallar
    """
    response = client.post('/api/auth/login', json={
        'email': 'client@test.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    assert 'error' in response.json

def test_login_nonexistent_user(client):
    """
    Test: Login con usuario inexistente debe fallar
    """
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@test.com',
        'password': 'password123'
    })
    
    assert response.status_code == 401
    assert 'error' in response.json

def test_login_missing_fields(client):
    """
    Test: Login sin campos requeridos debe fallar
    """
    response = client.post('/api/auth/login', json={
        'email': 'test@test.com'
        # Falta password
    })
    
    assert response.status_code == 400
    assert 'error' in response.json