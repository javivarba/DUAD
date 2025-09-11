#!/usr/bin/env python3
"""
Ejercicio 3: Script de Validación y Creación Condicional de Tablas
Valida si las tablas existen, y si no las crea automáticamente
"""

from sqlalchemy import (
    create_engine, 
    MetaData, 
    Table, 
    Column, 
    Integer, 
    String, 
    Text,
    ForeignKey,
    DateTime,
    Boolean,
    Numeric,
    inspect
)
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
import os
import sys

# ==========================================
# DEFINICIÓN DEL ESQUEMA (del ejercicio 2)
# ==========================================

def define_schema():
    """Define el esquema de la base de datos"""
    metadata = MetaData()
    
    # Tabla usuarios
    usuarios = Table(
        "usuarios",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("nombre", String(50), nullable=False),
        Column("apellido", String(50), nullable=False),
        Column("email", String(100), nullable=False, unique=True),
        Column("telefono", String(20)),
        Column("fecha_registro", DateTime, default=func.now()),
        Column("activo", Boolean, default=True)
    )
    
    # Tabla direcciones (FK obligatoria)
    direcciones = Table(
        "direcciones",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),
        Column("tipo_direccion", String(20), nullable=False),
        Column("calle", String(100), nullable=False),
        Column("numero", String(10)),
        Column("ciudad", String(50), nullable=False),
        Column("codigo_postal", String(10)),
        Column("pais", String(50), default="Costa Rica"),
        Column("direccion_principal", Boolean, default=False),
        Column("fecha_creacion", DateTime, default=func.now())
    )
    
    # Tabla automóviles (FK opcional)
    automoviles = Table(
        "automoviles",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=True),
        Column("marca", String(30), nullable=False),
        Column("modelo", String(50), nullable=False),
        Column("año", Integer, nullable=False),
        Column("color", String(20)),
        Column("placa", String(20), unique=True),
        Column("numero_chasis", String(50), unique=True),
        Column("precio", Numeric(10, 2)),
        Column("disponible", Boolean, default=True),
        Column("fecha_registro", DateTime, default=func.now()),
        Column("observaciones", Text)
    )
    
    return metadata

# ==========================================
# FUNCIONES DE VALIDACIÓN Y CREACIÓN
# ==========================================

def check_database_exists(database_uri):
    """Verifica si la base de datos existe (para SQLite)"""
    if database_uri.startswith("sqlite:///"):
        db_path = database_uri.replace("sqlite:///", "")
        if db_path != ":memory:":
            return os.path.exists(db_path)
    return True  # Para otras bases de datos asumimos que existen

def check_table_exists(engine, table_name):
    """Verifica si una tabla específica existe en la base de datos"""
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        return table_name in existing_tables
    except Exception as e:
        print(f"❌ Error verificando tabla {table_name}: {e}")
        return False

def get_existing_tables(engine):
    """Obtiene la lista de tablas existentes en la base de datos"""
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        print(f"❌ Error obteniendo tablas existentes: {e}")
        return []

def validate_and_create_tables(database_uri="sqlite:///ejercicio3_validacion.db"):
    """
    Función principal que valida y crea tablas según sea necesario
    """
    print("=" * 70)
    print("🔍 INICIANDO VALIDACIÓN Y CREACIÓN DE TABLAS")
    print("=" * 70)
    
    # Paso 1: Verificar si la base de datos existe
    db_exists = check_database_exists(database_uri)
    print(f"\n📊 Base de datos: {database_uri}")
    print(f"🔹 Existe: {'Sí' if db_exists else 'No (se creará)'}")
    
    try:
        # Paso 2: Crear engine y conectar
        print(f"\n🔌 Creando conexión...")
        engine = create_engine(database_uri, echo=False)  # echo=False para output más limpio
        
        # Paso 3: Obtener esquema definido
        metadata = define_schema()
        required_tables = list(metadata.tables.keys())
        print(f"📋 Tablas requeridas: {required_tables}")
        
        # Paso 4: Verificar tablas existentes
        print(f"\n🔍 VERIFICANDO TABLAS EXISTENTES...")
        existing_tables = get_existing_tables(engine)
        print(f"📋 Tablas encontradas: {existing_tables if existing_tables else 'Ninguna'}")
        
        # Paso 5: Analizar qué tablas faltan
        missing_tables = []
        existing_required_tables = []
        
        for table_name in required_tables:
            if check_table_exists(engine, table_name):
                existing_required_tables.append(table_name)
                print(f"✅ Tabla '{table_name}': EXISTE")
            else:
                missing_tables.append(table_name)
                print(f"❌ Tabla '{table_name}': NO EXISTE")
        
        # Paso 6: Crear tablas faltantes
        if missing_tables:
            print(f"\n🛠️  CREANDO TABLAS FALTANTES...")
            print(f"📝 Tablas a crear: {missing_tables}")
            
            # Crear solo las tablas que faltan
            metadata.create_all(engine, checkfirst=True)
            
            print(f"✅ Tablas creadas exitosamente!")
            
            # Verificar que se crearon correctamente
            print(f"\n🔍 VERIFICACIÓN POST-CREACIÓN...")
            for table_name in missing_tables:
                if check_table_exists(engine, table_name):
                    print(f"✅ Confirmado: Tabla '{table_name}' creada correctamente")
                else:
                    print(f"❌ Error: Tabla '{table_name}' no se pudo crear")
        else:
            print(f"\n✅ TODAS LAS TABLAS YA EXISTEN")
            print(f"🎉 No es necesario crear ninguna tabla")
        
        # Paso 7: Resumen final
        print(f"\n" + "=" * 70)
        print(f"📊 RESUMEN FINAL")
        print(f"=" * 70)
        
        final_tables = get_existing_tables(engine)
        print(f"🔹 Total de tablas en BD: {len(final_tables)}")
        print(f"🔹 Tablas existentes: {final_tables}")
        print(f"🔹 Tablas requeridas: {required_tables}")
        
        # Verificar que todas las tablas requeridas existen
        all_required_exist = all(table in final_tables for table in required_tables)
        if all_required_exist:
            print(f"✅ Estado: TODAS LAS TABLAS REQUERIDAS ESTÁN PRESENTES")
        else:
            print(f"❌ Estado: FALTAN TABLAS REQUERIDAS")
        
        return engine, all_required_exist
        
    except SQLAlchemyError as e:
        print(f"❌ Error de SQLAlchemy: {e}")
        return None, False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None, False

def demo_multiple_executions():
    """
    Demuestra múltiples ejecuciones del script para mostrar la validación
    """
    print("🎭 DEMOSTRACIÓN: MÚLTIPLES EJECUCIONES")
    print("=" * 70)
    
    db_uri = "sqlite:///demo_validacion.db"
    
    # Primera ejecución (creará las tablas)
    print("\n1️⃣  PRIMERA EJECUCIÓN (tablas no existen):")
    print("-" * 50)
    validate_and_create_tables(db_uri)
    
    # Segunda ejecución (tablas ya existen)
    print("\n\n2️⃣  SEGUNDA EJECUCIÓN (tablas ya existen):")
    print("-" * 50)
    validate_and_create_tables(db_uri)

if __name__ == "__main__":
    print("🚀 EJERCICIO 3: VALIDACIÓN Y CREACIÓN CONDICIONAL DE TABLAS")
    print("📝 Este script valida si las tablas existen y las crea si es necesario\n")
    
    # Ejecutar validación principal
    engine, success = validate_and_create_tables()
    
    if success:
        print(f"\n🎉 ¡EJERCICIO 3 COMPLETADO EXITOSAMENTE!")
        
        # Preguntar si quiere ver la demostración de múltiples ejecuciones
        print(f"\n💡 Para ver la demostración de múltiples ejecuciones,")
        print(f"   descomenta la línea al final del script.")
        
        # Descomentar la siguiente línea para ver la demostración:
        # demo_multiple_executions()
        
    else:
        print(f"\n❌ Hubo errores en la ejecución del ejercicio")
        sys.exit(1)