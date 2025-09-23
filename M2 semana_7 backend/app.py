from flask import Flask, request, Response, jsonify
from db import DB_Manager
from JWT_Manager import JWT_Manager
from auth_decorators import require_auth, require_role

app = Flask("fruits-api")

# Inicializar managers
db_manager = DB_Manager()
jwt_manager = JWT_Manager('keys/private_key.pem', 'keys/public_key.pem')

# === ENDPOINTS DE AUTENTICACIÓN ===
@app.route("/liveness")
def liveness():
    return "<p>Fruits API is running!</p>"

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return Response(status=400)
        
        # Por defecto los usuarios son "user", solo admins pueden crear otros admins
        role = data.get('role', 'user')
        
        result = db_manager.insert_user(
            data.get('username'),
            data.get('password'),
            role
        )
        
        user_id = result[0]
        token = jwt_manager.encode({'id': user_id, 'role': role})
        
        if token:
            return jsonify(token=token)
        else:
            return Response(status=500)
            
    except Exception as e:
        print(f"Register error: {e}")
        return Response(status=500)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return Response(status=400)
        
        user = db_manager.get_user(data.get('username'), data.get('password'))
        
        if user is None:
            return Response(status=403)  # Unauthorized - credenciales inválidas
        
        user_id = user[0]
        role = user[3]
        token = jwt_manager.encode({'id': user_id, 'role': role})
        
        if token:
            return jsonify(token=token)
        else:
            return Response(status=500)
            
    except Exception as e:
        print(f"Login error: {e}")
        return Response(status=500)

@app.route('/me')
@require_auth(db_manager, jwt_manager)
def me(user):
    try:
        return jsonify(
            id=user[0],
            username=user[1],
            role=user[3]
        )
    except Exception as e:
        print(f"Me error: {e}")
        return Response(status=500)

# === ENDPOINTS DE PRODUCTOS (Solo Admin) ===
@app.route('/products', methods=['GET'])
@require_role('admin', db_manager, jwt_manager)
def get_products(user):
    try:
        products = db_manager.get_all_products()
        products_list = []
        for p in products:
            products_list.append({
                'id': p[0],
                'name': p[1],
                'price': p[2],
                'entry_date': p[3].isoformat() if p[3] else None,
                'quantity': p[4]
            })
        return jsonify(products=products_list)
    except Exception as e:
        print(f"Get products error: {e}")
        return Response(status=500)

@app.route('/products/<int:product_id>', methods=['GET'])
@require_role('admin', db_manager, jwt_manager)
def get_product(user, product_id):
    try:
        product = db_manager.get_product_by_id(product_id)
        if product is None:
            return Response(status=404)
        
        return jsonify(
            id=product[0],
            name=product[1],
            price=product[2],
            entry_date=product[3].isoformat() if product[3] else None,
            quantity=product[4]
        )
    except Exception as e:
        print(f"Get product error: {e}")
        return Response(status=500)

@app.route('/products', methods=['POST'])
@require_role('admin', db_manager, jwt_manager)
def create_product(user):
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'price', 'quantity']):
            return Response(status=400)
        
        if data['price'] <= 0 or data['quantity'] < 0:
            return Response(status=400)
        
        result = db_manager.insert_product(
            data['name'],
            data['price'],
            data['quantity']
        )
        
        return jsonify(id=result[0], message="Product created successfully"), 201
    except Exception as e:
        print(f"Create product error: {e}")
        return Response(status=500)

@app.route('/products/<int:product_id>', methods=['PUT'])
@require_role('admin', db_manager, jwt_manager)
def update_product(user, product_id):
    try:
        data = request.get_json()
        if not data:
            return Response(status=400)
        
        # Verificar que el producto existe
        if db_manager.get_product_by_id(product_id) is None:
            return Response(status=404)
        
        success = db_manager.update_product(
            product_id,
            name=data.get('name'),
            price=data.get('price'),
            quantity=data.get('quantity')
        )
        
        if success:
            return jsonify(message="Product updated successfully")
        else:
            return Response(status=400)
            
    except Exception as e:
        print(f"Update product error: {e}")
        return Response(status=500)

@app.route('/products/<int:product_id>', methods=['DELETE'])
@require_role('admin', db_manager, jwt_manager)
def delete_product(user, product_id):
    try:
        success = db_manager.delete_product(product_id)
        if success:
            return jsonify(message="Product deleted successfully")
        else:
            return Response(status=404)
    except Exception as e:
        print(f"Delete product error: {e}")
        return Response(status=500)

# === ENDPOINT DE COMPRA (Usuario y Admin) ===
@app.route('/purchase', methods=['POST'])
@require_auth(db_manager, jwt_manager)
def purchase_product(user):
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['product_id', 'quantity']):
            return Response(status=400)
        
        product_id = data['product_id']
        quantity = data['quantity']
        
        if quantity <= 0:
            return Response(status=400)
        
        # Obtener producto
        product = db_manager.get_product_by_id(product_id)
        if product is None:
            return Response(status=404)
        
        # Verificar stock
        if product[4] < quantity:  # product[4] es quantity
            return jsonify(error="Insufficient stock"), 400
        
        # Calcular totales
        product_price = product[2]
        total_price = product_price * quantity
        
        # Reducir stock
        db_manager.reduce_product_quantity(product_id, quantity)
        
        # Crear factura
        invoice_id = db_manager.insert_invoice(
            user[0],  # user_id
            product[1],  # product_name
            product_price,
            quantity,
            total_price
        )
        
        return jsonify(
            message="Purchase successful",
            invoice_id=invoice_id[0],
            total_price=total_price
        ), 201
        
    except Exception as e:
        print(f"Purchase error: {e}")
        return Response(status=500)

# === ENDPOINT DE FACTURAS (Usuario y Admin) ===
@app.route('/invoices', methods=['GET'])
@require_auth(db_manager, jwt_manager)
def get_invoices(user):
    try:
        invoices = db_manager.get_invoices_by_user(user[0])
        invoices_list = []
        
        for inv in invoices:
            invoices_list.append({
                'id': inv[0],
                'product_name': inv[2],
                'product_price': inv[3],
                'quantity': inv[4],
                'total_price': inv[5],
                'purchase_date': inv[6].isoformat() if inv[6] else None
            })
        
        return jsonify(invoices=invoices_list)
    except Exception as e:
        print(f"Get invoices error: {e}")
        return Response(status=500)

if __name__ == '__main__':
    app.run(debug=True)


# Test JWT (temporal)
@app.route('/test-jwt')
def test_jwt():
    test_token = jwt_manager.encode({'id': 1, 'role': 'admin'})
    return jsonify(token_generated=test_token is not None, token=test_token)