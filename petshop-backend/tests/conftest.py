import pytest
from app import create_app, db
from app.models import User, Product, PaymentMethod

@pytest.fixture
def app():
    """
    Crea una instancia de la aplicación para testing
    """
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Cliente de prueba para hacer requests
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Runner para comandos CLI
    """
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    """
    Crea un usuario administrador para tests
    """
    user = User(
        email='admin@test.com',
        first_name='Admin',
        last_name='Test',
        role='admin'
    )
    user.set_password('admin123')
    
    db.session.add(user)
    db.session.commit()
    
    return user

@pytest.fixture
def client_user(app):
    """
    Crea un usuario cliente para tests
    """
    user = User(
        email='client@test.com',
        first_name='Client',
        last_name='Test',
        role='client'
    )
    user.set_password('client123')
    
    db.session.add(user)
    db.session.commit()
    
    return user

@pytest.fixture
def sample_product(app):
    """
    Crea un producto de ejemplo para tests
    """
    product = Product(
        name='Alimento para perros',
        description='Alimento premium',
        price=25000,
        stock=100,
        category='alimento'
    )
    
    db.session.add(product)
    db.session.commit()
    
    return product

@pytest.fixture
def payment_method(app):
    """
    Crea un método de pago para tests
    """
    pm = PaymentMethod(
        name='SINPE Móvil',
        description='Transferencia SINPE',
        is_active=True
    )
    
    db.session.add(pm)
    db.session.commit()
    
    return pm

@pytest.fixture
def admin_token(client, admin_user):
    """
    Obtiene un token JWT para el admin
    """
    response = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'admin123'
    })
    
    return response.json['access_token']

@pytest.fixture
def client_token(client, client_user):
    """
    Obtiene un token JWT para el cliente
    """
    response = client.post('/api/auth/login', json={
        'email': 'client@test.com',
        'password': 'client123'
    })
    
    return response.json['access_token']