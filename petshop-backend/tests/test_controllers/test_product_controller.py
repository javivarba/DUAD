import pytest

def test_get_all_products_public(client, sample_product):
    """
    Test: Obtener todos los productos (endpoint público)
    """
    response = client.get('/api/products/')
    
    assert response.status_code == 200
    assert 'products' in response.json
    assert len(response.json['products']) >= 1

def test_get_product_by_id_public(client, sample_product):
    """
    Test: Obtener producto por ID (endpoint público)
    """
    response = client.get(f'/api/products/{sample_product.id}')
    
    assert response.status_code == 200
    assert response.json['id'] == sample_product.id
    assert response.json['name'] == 'Alimento para perros'

def test_get_product_not_found(client):
    """
    Test: Obtener producto inexistente debe retornar 404
    """
    response = client.get('/api/products/99999')
    
    assert response.status_code == 404
    assert 'error' in response.json

def test_create_product_as_admin(client, admin_token):
    """
    Test: Admin puede crear productos
    """
    response = client.post('/api/products/', 
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Juguete para gatos',
            'price': 5000,
            'stock': 50,
            'category': 'juguete'
        }
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.data}")
    
    assert response.status_code == 201

def test_create_product_without_auth(client):
    """
    Test: Crear producto sin autenticación debe fallar
    """
    response = client.post('/api/products/', json={
        'name': 'Producto sin auth',
        'price': 1000,
        'stock': 10
    })
    
    assert response.status_code == 401

def test_create_product_as_client(client, client_token):
    """
    Test: Cliente no puede crear productos
    """
    response = client.post('/api/products/',
        headers={'Authorization': f'Bearer {client_token}'},
        json={
            'name': 'Producto de cliente',
            'price': 1000,
            'stock': 10
        }
    )
    
    assert response.status_code == 403
    assert 'error' in response.json

def test_create_product_missing_fields(client, admin_token):
    """
    Test: Crear producto sin campos requeridos debe fallar
    """
    response = client.post('/api/products/',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Producto incompleto'
            # Faltan price y stock
        }
    )
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_update_product_as_admin(client, admin_token, sample_product):
    """
    Test: Admin puede actualizar productos
    """
    response = client.put(f'/api/products/{sample_product.id}',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={
            'name': 'Alimento Premium Actualizado',
            'price': 30000
        }
    )
    
    assert response.status_code == 200
    assert response.json['product']['name'] == 'Alimento Premium Actualizado'
    assert float(response.json['product']['price']) == 30000

def test_update_product_as_client(client, client_token, sample_product):
    """
    Test: Cliente no puede actualizar productos
    """
    response = client.put(f'/api/products/{sample_product.id}',
        headers={'Authorization': f'Bearer {client_token}'},
        json={'name': 'Intento de actualización'}
    )
    
    assert response.status_code == 403

def test_delete_product_as_admin(client, admin_token, sample_product):
    """
    Test: Admin puede eliminar productos
    """
    response = client.delete(f'/api/products/{sample_product.id}',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    
    assert response.status_code == 200
    assert response.json['message'] == 'Producto eliminado exitosamente'
    
    # Verificar que ya no existe
    get_response = client.get(f'/api/products/{sample_product.id}')
    assert get_response.status_code == 404

def test_delete_product_as_client(client, client_token, sample_product):
    """
    Test: Cliente no puede eliminar productos
    """
    response = client.delete(f'/api/products/{sample_product.id}',
        headers={'Authorization': f'Bearer {client_token}'}
    )
    
    assert response.status_code == 403

def test_update_stock_as_admin(client, admin_token, sample_product):
    """
    Test: Admin puede actualizar stock
    """
    initial_stock = sample_product.stock  # Guardar stock inicial
    
    response = client.patch(f'/api/products/{sample_product.id}/stock',
        headers={'Authorization': f'Bearer {admin_token}'},
        json={'quantity': 20}
    )
    
    assert response.status_code == 200
    assert response.json['product']['stock'] == initial_stock + 20