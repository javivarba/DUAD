#!/usr/bin/env python3
"""
SQLAlchemy Setup and Verification Script
Ejercicio 1: Verificación de instalación de SQLAlchemy
"""

import sqlalchemy
from sqlalchemy import create_engine, text
import sys

def verify_sqlalchemy_installation():
    """Verifica que SQLAlchemy esté correctamente instalado"""
    
    print("=" * 50)
    print("VERIFICACIÓN DE SQLALCHEMY")
    print("=" * 50)
    
    # 1. Verificar versión de SQLAlchemy
    print(f"✅ SQLAlchemy version: {sqlalchemy.__version__}")
    
    # 2. Verificar versión de Python
    print(f"✅ Python version: {sys.version}")
    
    # 3. Verificar que podemos crear un engine (con SQLite para prueba)
    try:
        # Usamos SQLite en memoria para la prueba (no requiere instalación adicional)
        engine = create_engine("sqlite:///:memory:", echo=True)
        print("✅ Engine creation: SUCCESS")
        
        # 4. Verificar que podemos hacer una conexión básica
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'SQLAlchemy is working!' as message"))
            message = result.fetchone()
            print(f"✅ Test query: {message[0]}")
            
    except Exception as e:
        print(f"❌ Error en la conexión: {e}")
        return False
    
    print("=" * 50)
    print("🎉 SETUP COMPLETADO EXITOSAMENTE")
    print("=" * 50)
    
    return True

def check_postgresql_driver():
    """Verifica si el driver de PostgreSQL está disponible"""
    try:
        import psycopg2
        print(f"✅ psycopg2 version: {psycopg2.__version__}")
        return True
    except ImportError:
        print("⚠️  psycopg2 no está instalado (opcional para PostgreSQL)")
        print("   Instalar con: pip install psycopg2-binary")
        return False

if __name__ == "__main__":
    print("Iniciando verificación de SQLAlchemy...")
    
    # Verificar instalación básica
    setup_ok = verify_sqlalchemy_installation()
    
    # Verificar driver de PostgreSQL (opcional)
    print("\nVerificando drivers adicionales:")
    check_postgresql_driver()
    
    if setup_ok:
        print("\n🚀 ¡Listo para comenzar con los ejercicios de ORM!")
    else:
        print("\n❌ Hay problemas con el setup. Revisa la instalación.")