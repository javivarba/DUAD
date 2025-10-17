from app import create_app, db
import os

# Obtener el ambiente desde variable de entorno
config_name = os.getenv('FLASK_ENV', 'development')

# Crear la aplicación
app = create_app(config_name)

if __name__ == '__main__':
    # Comentamos esto temporalmente hasta tener modelos
    # with app.app_context():
    #     db.create_all()
    
    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )