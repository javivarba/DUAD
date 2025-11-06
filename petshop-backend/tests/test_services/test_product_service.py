import pytest
from app.services import ProductService
from werkzeug.exceptions import BadRequest, NotFound

def test_create_product_success(app):
    """
    Test: Crear un producto exitosamente
    """
    product = ProductService.create_product(
        name='Juguete para gatos',
        price=5000,
        stock=50,
        description='Juguete interactivo',
        category='juguete'
    )
    
    assert product.id is not None
    assert product.name == 'Juguete para gatos'
    assert float(product.price) == 5000
    assert product.stock == 50
    assert product.category == 'juguete'

def test_create_product_invalid_price(app):
    """
    Test: Crear producto con precio negativo debe fallar
    """
    with pytest.raises(BadRequest):
        ProductService.create_product(
            name='Producto inválido',
            price=-100,
            stock=10
        )

def test_create_product_invalid_stock(app):
    """
    Test: Crear producto con stock negativo debe fallar
    """
    with pytest.raises(BadRequest):
        ProductService.create_product(
            name='Producto inválido',
            price=1000,
            stock=-5
        )

def test_get_product_by_id_success(app, sample_product):
    """
    Test: Obtener producto por ID exitosamente
    """
    product = ProductService.get_product_by_id(sample_product.id)
    
    assert product.id == sample_product.id
    assert product.name == 'Alimento para perros'

def test_get_product_by_id_not_found(app):
    """
    Test: Obtener producto inexistente debe fallar
    """
    with pytest.raises(NotFound):
        ProductService.get_product_by_id(99999)

def test_get_all_products(app, sample_product):
    """
    Test: Obtener todos los productos
    """
    products = ProductService.get_all_products()
    
    assert len(products) >= 1
    assert any(p.id == sample_product.id for p in products)

def test_get_products_by_category(app, sample_product):
    """
    Test: Filtrar productos por categoría
    """
    products = ProductService.get_all_products(category='alimento')
    
    assert len(products) >= 1
    assert all(p.category == 'alimento' for p in products)

def test_update_product_success(app, sample_product):
    """
    Test: Actualizar producto exitosamente
    """
    updated_product = ProductService.update_product(
        sample_product.id,
        name='Alimento Premium',
        price=30000
    )
    
    assert updated_product.name == 'Alimento Premium'
    assert float(updated_product.price) == 30000

def test_update_product_invalid_price(app, sample_product):
    """
    Test: Actualizar producto con precio inválido debe fallar
    """
    with pytest.raises(BadRequest):
        ProductService.update_product(
            sample_product.id,
            price=-100
        )

def test_update_stock_add(app, sample_product):
    """
    Test: Agregar stock a un producto
    """
    initial_stock = sample_product.stock
    product = ProductService.update_stock(sample_product.id, 20)
    
    assert product.stock == initial_stock + 20

def test_update_stock_reduce(app, sample_product):
    """
    Test: Reducir stock de un producto
    """
    initial_stock = sample_product.stock
    product = ProductService.update_stock(sample_product.id, -10)
    
    assert product.stock == initial_stock - 10

def test_update_stock_insufficient(app, sample_product):
    """
    Test: Reducir más stock del disponible debe fallar
    """
    with pytest.raises(BadRequest):
        ProductService.update_stock(sample_product.id, -1000)

def test_check_stock_availability_success(app, sample_product):
    """
    Test: Verificar disponibilidad de stock exitosamente
    """
    result = ProductService.check_stock_availability(sample_product.id, 50)
    
    assert result is True

def test_check_stock_availability_insufficient(app, sample_product):
    """
    Test: Verificar stock insuficiente
    """
    result = ProductService.check_stock_availability(sample_product.id, 1000)
    
    assert result is False

def test_delete_product_success(app, sample_product):
    """
    Test: Eliminar producto exitosamente
    """
    result = ProductService.delete_product(sample_product.id)
    
    assert result is True
    
    # Verificar que el producto ya no existe
    with pytest.raises(NotFound):
        ProductService.get_product_by_id(sample_product.id)