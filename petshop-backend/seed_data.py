"""
Script para poblar la base de datos con datos de prueba
Ejecutar: python seed_data.py
"""

from app import create_app, db
from app.models import (
    User, Product, PaymentMethod, Address, 
    Cart, CartItem, Order, OrderItem, Invoice
)
from app.services import OrderService, CartService
from datetime import datetime

def clear_data():
    """
    Limpia todos los datos de la base de datos
    ⚠️ CUIDADO: Esto elimina TODOS los datos
    """
    print("🗑️  Limpiando datos existentes...")
    
    # Orden importante por las relaciones de foreign keys
    Invoice.query.delete()
    OrderItem.query.delete()
    Order.query.delete()
    CartItem.query.delete()
    Cart.query.delete()
    Address.query.delete()
    Product.query.delete()
    PaymentMethod.query.delete()
    User.query.delete()
    
    db.session.commit()
    print("✅ Datos limpiados exitosamente\n")

def create_users():
    """
    Crea 1 admin y 3 clientes
    """
    print("👥 Creando usuarios...")
    
    users = []
    
    # Admin
    admin = User(
        email='admin@petshop.com',
        first_name='Admin',
        last_name='Principal',
        role='admin'
    )
    admin.set_password('admin123')
    users.append(admin)
    
    # Clientes
    clients_data = [
        {
            'email': 'juan.perez@email.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'password': 'client123'
        },
        {
            'email': 'maria.rodriguez@email.com',
            'first_name': 'María',
            'last_name': 'Rodríguez',
            'password': 'client123'
        },
        {
            'email': 'carlos.gonzalez@email.com',
            'first_name': 'Carlos',
            'last_name': 'González',
            'password': 'client123'
        }
    ]
    
    for client_data in clients_data:
        client = User(
            email=client_data['email'],
            first_name=client_data['first_name'],
            last_name=client_data['last_name'],
            role='client'
        )
        client.set_password(client_data['password'])
        users.append(client)
    
    db.session.add_all(users)
    db.session.commit()
    
    print(f"✅ {len(users)} usuarios creados")
    print(f"   - Admin: admin@petshop.com / admin123")
    for client_data in clients_data:
        print(f"   - Cliente: {client_data['email']} / client123")
    print()
    
    return users

def create_payment_methods():
    """
    Crea 4 métodos de pago
    """
    print("💳 Creando métodos de pago...")
    
    payment_methods_data = [
        {
            'name': 'SINPE Móvil',
            'description': 'Transferencia instantánea mediante SINPE Móvil',
            'is_active': True
        },
        {
            'name': 'Tarjeta de Crédito/Débito',
            'description': 'Pago con tarjeta Visa, Mastercard o American Express',
            'is_active': True
        },
        {
            'name': 'Efectivo',
            'description': 'Pago en efectivo contra entrega',
            'is_active': True
        },
        {
            'name': 'Transferencia Bancaria',
            'description': 'Transferencia bancaria tradicional',
            'is_active': True
        }
    ]
    
    payment_methods = []
    for pm_data in payment_methods_data:
        pm = PaymentMethod(**pm_data)
        payment_methods.append(pm)
    
    db.session.add_all(payment_methods)
    db.session.commit()
    
    print(f"✅ {len(payment_methods)} métodos de pago creados")
    for pm in payment_methods:
        print(f"   - {pm.name}")
    print()
    
    return payment_methods

def create_products():
    """
    Crea 15 productos de diferentes categorías
    """
    print("🏷️  Creando productos...")
    
    products_data = [
        # Alimentos (5 productos)
        {
            'name': 'Alimento Premium para Perros Adultos',
            'description': 'Alimento balanceado de alta calidad para perros adultos de todas las razas. Rico en proteínas y vitaminas.',
            'price': 28500,
            'stock': 50,
            'category': 'alimento',
            'image_url': 'https://example.com/dog-food-premium.jpg'
        },
        {
            'name': 'Alimento para Gatos Adultos',
            'description': 'Alimento completo para gatos adultos con omega 3 y 6',
            'price': 22000,
            'stock': 40,
            'category': 'alimento',
            'image_url': 'https://example.com/cat-food.jpg'
        },
        {
            'name': 'Snacks Dentales para Perros',
            'description': 'Galletas que ayudan a limpiar los dientes y refrescar el aliento',
            'price': 4500,
            'stock': 100,
            'category': 'alimento',
            'image_url': 'https://example.com/dental-treats.jpg'
        },
        {
            'name': 'Alimento para Cachorros',
            'description': 'Nutrición especial para cachorros en crecimiento',
            'price': 32000,
            'stock': 35,
            'category': 'alimento',
            'image_url': 'https://example.com/puppy-food.jpg'
        },
        {
            'name': 'Alimento para Gatos Gatitos',
            'description': 'Fórmula especial para gatitos de 2 a 12 meses',
            'price': 25000,
            'stock': 30,
            'category': 'alimento',
            'image_url': 'https://example.com/kitten-food.jpg'
        },
        
        # Juguetes (4 productos)
        {
            'name': 'Pelota de Goma Resistente',
            'description': 'Pelota indestructible para perros de todas las razas',
            'price': 3500,
            'stock': 80,
            'category': 'juguete',
            'image_url': 'https://example.com/rubber-ball.jpg'
        },
        {
            'name': 'Ratón de Juguete para Gatos',
            'description': 'Ratón con catnip que estimula el instinto de caza',
            'price': 2000,
            'stock': 120,
            'category': 'juguete',
            'image_url': 'https://example.com/cat-mouse.jpg'
        },
        {
            'name': 'Cuerda para Perros',
            'description': 'Cuerda de algodón trenzado para jugar y limpiar dientes',
            'price': 4000,
            'stock': 60,
            'category': 'juguete',
            'image_url': 'https://example.com/rope-toy.jpg'
        },
        {
            'name': 'Láser Interactivo para Gatos',
            'description': 'Puntero láser con patrones automáticos',
            'price': 8500,
            'stock': 25,
            'category': 'juguete',
            'image_url': 'https://example.com/laser-toy.jpg'
        },
        
        # Accesorios (3 productos)
        {
            'name': 'Collar Ajustable para Perros',
            'description': 'Collar de nylon resistente con hebilla de seguridad',
            'price': 5500,
            'stock': 45,
            'category': 'accesorio',
            'image_url': 'https://example.com/dog-collar.jpg'
        },
        {
            'name': 'Cama Acolchada para Gatos',
            'description': 'Cama suave y cómoda con cojín removible',
            'price': 15000,
            'stock': 20,
            'category': 'accesorio',
            'image_url': 'https://example.com/cat-bed.jpg'
        },
        {
            'name': 'Transportadora para Mascotas',
            'description': 'Transportadora rígida con ventilación y seguro',
            'price': 25000,
            'stock': 15,
            'category': 'accesorio',
            'image_url': 'https://example.com/carrier.jpg'
        },
        
        # Higiene (2 productos)
        {
            'name': 'Shampoo para Perros',
            'description': 'Shampoo hipoalergénico con acondicionador incluido',
            'price': 8000,
            'stock': 55,
            'category': 'higiene',
            'image_url': 'https://example.com/dog-shampoo.jpg'
        },
        {
            'name': 'Arena Aglomerante para Gatos',
            'description': 'Arena de alta absorción que controla olores',
            'price': 12000,
            'stock': 40,
            'category': 'higiene',
            'image_url': 'https://example.com/cat-litter.jpg'
        },
        
        # Medicina (1 producto)
        {
            'name': 'Antiparasitario Externo',
            'description': 'Pipeta antiparasitaria de acción prolongada',
            'price': 18000,
            'stock': 30,
            'category': 'medicina',
            'image_url': 'https://example.com/antiparasitic.jpg'
        }
    ]
    
    products = []
    for prod_data in products_data:
        product = Product(**prod_data)
        products.append(product)
    
    db.session.add_all(products)
    db.session.commit()
    
    print(f"✅ {len(products)} productos creados")
    
    # Contar por categoría
    categories = {}
    for product in products:
        categories[product.category] = categories.get(product.category, 0) + 1
    
    for category, count in categories.items():
        print(f"   - {category.capitalize()}: {count} productos")
    print()
    
    return products

def create_addresses(users):
    """
    Crea direcciones para los clientes (no para el admin)
    """
    print("📍 Creando direcciones...")
    
    # Solo crear direcciones para los clientes (índices 1, 2, 3)
    addresses_data = [
        # Direcciones para Juan Pérez (user index 1)
        [
            {
                'full_name': 'Juan Pérez',
                'phone': '88887777',
                'address_line1': 'Calle 15, Avenida 3',
                'address_line2': 'Apartamento 201',
                'city': 'San José',
                'state': 'San José',
                'postal_code': '10101',
                'country': 'Costa Rica',
                'is_default': True
            },
            {
                'full_name': 'Juan Pérez',
                'phone': '88887777',
                'address_line1': 'Oficina Central, Edificio Torre B',
                'address_line2': 'Piso 5',
                'city': 'Escazú',
                'state': 'San José',
                'postal_code': '10203',
                'country': 'Costa Rica',
                'is_default': False
            }
        ],
        # Direcciones para María Rodríguez (user index 2)
        [
            {
                'full_name': 'María Rodríguez',
                'phone': '89991234',
                'address_line1': 'Barrio Escalante, Casa 45',
                'address_line2': 'Portón verde',
                'city': 'San José',
                'state': 'San José',
                'postal_code': '10102',
                'country': 'Costa Rica',
                'is_default': True
            }
        ],
        # Direcciones para Carlos González (user index 3)
        [
            {
                'full_name': 'Carlos González',
                'phone': '87776655',
                'address_line1': 'Residencial Los Pinos, Casa 12',
                'address_line2': None,
                'city': 'Heredia',
                'state': 'Heredia',
                'postal_code': '40101',
                'country': 'Costa Rica',
                'is_default': True
            }
        ]
    ]
    
    addresses = []
    for i, user_addresses in enumerate(addresses_data):
        user = users[i + 1]  # +1 porque el admin es el índice 0
        for addr_data in user_addresses:
            address = Address(user_id=user.id, **addr_data)
            addresses.append(address)
    
    db.session.add_all(addresses)
    db.session.commit()
    
    print(f"✅ {len(addresses)} direcciones creadas")
    for i, count in enumerate([2, 1, 1]):
        print(f"   - {users[i+1].first_name}: {count} dirección(es)")
    print()
    
    return addresses

def create_sample_orders(users, products, payment_methods, addresses):
    """
    Crea algunas órdenes de ejemplo con sus facturas
    """
    print("📦 Creando órdenes de ejemplo...")
    
    # Obtener clientes (sin admin)
    clients = users[1:]  # Índices 1, 2, 3
    
    orders_created = 0
    
    # Orden 1: Juan Pérez compra alimento y juguete para perro
    print("   Creando orden 1...")
    juan = clients[0]
    juan_address = Address.query.filter_by(user_id=juan.id, is_default=True).first()
    
    # Crear carrito para Juan
    juan_cart = Cart(user_id=juan.id, status='active')
    db.session.add(juan_cart)
    db.session.commit()
    
    # Agregar items al carrito (Alimento Premium + Pelota)
    cart_items = [
        CartItem(
            cart_id=juan_cart.id,
            product_id=products[0].id,  # Alimento Premium
            quantity=2,
            unit_price=products[0].price
        ),
        CartItem(
            cart_id=juan_cart.id,
            product_id=products[5].id,  # Pelota
            quantity=1,
            unit_price=products[5].price
        )
    ]
    db.session.add_all(cart_items)
    db.session.commit()
    
    # Crear orden
    try:
        order1 = OrderService.create_order_from_cart(
            user_id=juan.id,
            cart_id=juan_cart.id,
            address_id=juan_address.id,
            payment_method_id=payment_methods[0].id  # SINPE
        )
        orders_created += 1
        print(f"   ✅ Orden creada: {order1.invoice.invoice_number}")
    except Exception as e:
        print(f"   ❌ Error creando orden 1: {str(e)}")
        db.session.rollback()
    
    # Orden 2: María Rodríguez compra productos para gatos
    print("   Creando orden 2...")
    maria = clients[1]
    maria_address = Address.query.filter_by(user_id=maria.id, is_default=True).first()
    
    # Crear carrito para María
    maria_cart = Cart(user_id=maria.id, status='active')
    db.session.add(maria_cart)
    db.session.commit()
    
    # Agregar items (Alimento gatos + Ratón juguete + Arena)
    cart_items = [
        CartItem(
            cart_id=maria_cart.id,
            product_id=products[1].id,  # Alimento gatos
            quantity=1,
            unit_price=products[1].price
        ),
        CartItem(
            cart_id=maria_cart.id,
            product_id=products[6].id,  # Ratón juguete
            quantity=2,
            unit_price=products[6].price
        ),
        CartItem(
            cart_id=maria_cart.id,
            product_id=products[13].id,  # Arena
            quantity=1,
            unit_price=products[13].price
        )
    ]
    db.session.add_all(cart_items)
    db.session.commit()
    
    try:
        order2 = OrderService.create_order_from_cart(
            user_id=maria.id,
            cart_id=maria_cart.id,
            address_id=maria_address.id,
            payment_method_id=payment_methods[1].id  # Tarjeta
        )
        orders_created += 1
        print(f"   ✅ Orden creada: {order2.invoice.invoice_number}")
    except Exception as e:
        print(f"   ❌ Error creando orden 2: {str(e)}")
        db.session.rollback()
    
    # Orden 3: Carlos González compra accesorios
    print("   Creando orden 3...")
    carlos = clients[2]
    carlos_address = Address.query.filter_by(user_id=carlos.id, is_default=True).first()
    
    # Crear carrito para Carlos
    carlos_cart = Cart(user_id=carlos.id, status='active')
    db.session.add(carlos_cart)
    db.session.commit()
    
    # Agregar items (Collar + Transportadora + Shampoo)
    cart_items = [
        CartItem(
            cart_id=carlos_cart.id,
            product_id=products[9].id,  # Collar
            quantity=1,
            unit_price=products[9].price
        ),
        CartItem(
            cart_id=carlos_cart.id,
            product_id=products[11].id,  # Transportadora
            quantity=1,
            unit_price=products[11].price
        ),
        CartItem(
            cart_id=carlos_cart.id,
            product_id=products[12].id,  # Shampoo
            quantity=1,
            unit_price=products[12].price
        )
    ]
    db.session.add_all(cart_items)
    db.session.commit()
    
    try:
        order3 = OrderService.create_order_from_cart(
            user_id=carlos.id,
            cart_id=carlos_cart.id,
            address_id=carlos_address.id,
            payment_method_id=payment_methods[2].id  # Efectivo
        )
        orders_created += 1
        print(f"   ✅ Orden creada: {order3.invoice.invoice_number}")
    except Exception as e:
        print(f"   ❌ Error creando orden 3: {str(e)}")
        db.session.rollback()
    
    print(f"✅ {orders_created} órdenes creadas con sus facturas\n")

def create_active_carts(users, products):
    """
    Crea carritos activos para algunos usuarios
    """
    print("🛒 Creando carritos activos...")
    
    # Juan tiene items en su nuevo carrito
    juan = users[1]
    juan_cart = Cart(user_id=juan.id, status='active')
    db.session.add(juan_cart)
    db.session.commit()
    
    cart_items = [
        CartItem(
            cart_id=juan_cart.id,
            product_id=products[3].id,  # Alimento cachorros
            quantity=1,
            unit_price=products[3].price
        )
    ]
    db.session.add_all(cart_items)
    db.session.commit()
    
    print(f"✅ Carrito activo creado para {juan.first_name}")
    print(f"   - 1 item en el carrito\n")

def main():
    """
    Función principal que ejecuta todo el proceso
    """
    print("=" * 60)
    print("🌱 SEED DATA - PETSHOP E-COMMERCE")
    print("=" * 60)
    print()
    
    # Crear app context
    app = create_app('development')
    
    with app.app_context():
        # Preguntar si limpiar datos
        response = input("⚠️  ¿Deseas limpiar los datos existentes? (s/n): ").lower()
        if response == 's':
            clear_data()
        
        # Crear datos en orden
        users = create_users()
        payment_methods = create_payment_methods()
        products = create_products()
        addresses = create_addresses(users)
        create_sample_orders(users, products, payment_methods, addresses)
        create_active_carts(users, products)
        
        # Resumen final
        print("=" * 60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print()
        print("📊 RESUMEN DE DATOS CREADOS:")
        print(f"   👥 Usuarios: {User.query.count()} (1 admin + 3 clientes)")
        print(f"   🏷️  Productos: {Product.query.count()}")
        print(f"   💳 Métodos de pago: {PaymentMethod.query.count()}")
        print(f"   📍 Direcciones: {Address.query.count()}")
        print(f"   🛒 Carritos: {Cart.query.count()}")
        print(f"   📦 Órdenes: {Order.query.count()}")
        print(f"   📄 Facturas: {Invoice.query.count()}")
        print()
        print("🔑 CREDENCIALES DE ACCESO:")
        print("   Admin:")
        print("     Email: admin@petshop.com")
        print("     Password: admin123")
        print()
        print("   Clientes:")
        print("     Email: juan.perez@email.com")
        print("     Email: maria.rodriguez@email.com")
        print("     Email: carlos.gonzalez@email.com")
        print("     Password (todos): client123")
        print()
        print("🚀 El servidor está listo para usarse!")
        print()

if __name__ == '__main__':
    main()