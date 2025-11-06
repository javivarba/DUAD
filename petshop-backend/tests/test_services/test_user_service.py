import pytest
from app.services import UserService
from werkzeug.exceptions import Conflict, BadRequest, NotFound

def test_create_user_success(app):
    """
    Test: Crear un usuario exitosamente
    """
    user = UserService.create_user(
        email='newuser@test.com',
        password='password123',
        first_name='New',
        last_name='User',
        role='client'
    )
    
    assert user.id is not None
    assert user.email == 'newuser@test.com'
    assert user.first_name == 'New'
    assert user.last_name == 'User'
    assert user.role == 'client'
    assert user.check_password('password123') is True

def test_create_user_duplicate_email(app, client_user):
    """
    Test: Intentar crear usuario con email duplicado debe fallar
    """
    with pytest.raises(Conflict):
        UserService.create_user(
            email='client@test.com',  # Email ya existe
            password='password123',
            first_name='Duplicate',
            last_name='User'
        )

def test_create_user_invalid_role(app):
    """
    Test: Crear usuario con rol inválido debe fallar
    """
    with pytest.raises(BadRequest):
        UserService.create_user(
            email='invalid@test.com',
            password='password123',
            first_name='Invalid',
            last_name='Role',
            role='superuser'  # Rol inválido
        )

def test_authenticate_success(app, client_user):
    """
    Test: Autenticación exitosa con credenciales correctas
    """
    user = UserService.authenticate('client@test.com', 'client123')
    
    assert user is not None
    assert user.email == 'client@test.com'

def test_authenticate_wrong_password(app, client_user):
    """
    Test: Autenticación con contraseña incorrecta debe fallar
    """
    with pytest.raises(BadRequest):
        UserService.authenticate('client@test.com', 'wrongpassword')

def test_authenticate_nonexistent_user(app):
    """
    Test: Autenticación con usuario que no existe debe fallar
    """
    with pytest.raises(BadRequest):
        UserService.authenticate('nonexistent@test.com', 'password123')

def test_get_user_by_id_success(app, client_user):
    """
    Test: Obtener usuario por ID exitosamente
    """
    user = UserService.get_user_by_id(client_user.id)
    
    assert user.id == client_user.id
    assert user.email == 'client@test.com'

def test_get_user_by_id_not_found(app):
    """
    Test: Obtener usuario inexistente debe fallar
    """
    with pytest.raises(NotFound):
        UserService.get_user_by_id(99999)

def test_update_user_success(app, client_user):
    """
    Test: Actualizar información del usuario exitosamente
    """
    updated_user = UserService.update_user(
        client_user.id,
        first_name='Updated',
        last_name='Name'
    )
    
    assert updated_user.first_name == 'Updated'
    assert updated_user.last_name == 'Name'
    assert updated_user.email == 'client@test.com'  # Email no cambió

def test_change_password_success(app, client_user):
    """
    Test: Cambiar contraseña exitosamente
    """
    user = UserService.change_password(
        client_user.id,
        'client123',  # Contraseña actual
        'newpassword123'  # Nueva contraseña
    )
    
    assert user.check_password('newpassword123') is True
    assert user.check_password('client123') is False

def test_change_password_wrong_old_password(app, client_user):
    """
    Test: Cambiar contraseña con contraseña actual incorrecta debe fallar
    """
    with pytest.raises(BadRequest):
        UserService.change_password(
            client_user.id,
            'wrongpassword',
            'newpassword123'
        )

def test_delete_user_success(app, client_user):
    """
    Test: Eliminar usuario exitosamente
    """
    result = UserService.delete_user(client_user.id)
    
    assert result is True
    
    # Verificar que el usuario ya no existe
    with pytest.raises(NotFound):
        UserService.get_user_by_id(client_user.id)