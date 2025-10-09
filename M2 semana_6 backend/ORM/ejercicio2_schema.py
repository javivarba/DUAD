#!/usr/bin/env python3
"""
Ejercicio 2: Diseño de Base de Datos con SQLAlchemy
Tablas: usuarios, direcciones, automóviles con sus respectivas relaciones
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
    Numeric
)
from sqlalchemy.sql import func
import datetime

# Crear objeto metadata
metadata_obj = MetaData()

# ==========================================
# TABLA USUARIOS (Tabla principal)
# ==========================================
usuarios_table = Table(
    "usuarios",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50), nullable=False),
    Column("apellido", String(50), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("telefono", String(20)),
    Column("fecha_registro", DateTime, default=func.now()),
    Column("activo", Boolean, default=True)
)

# ==========================================
# TABLA DIRECCIONES (FK obligatoria a usuarios)
# ==========================================
direcciones_table = Table(
    "direcciones",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),  # FK OBLIGATORIA
    Column("tipo_direccion", String(20), nullable=False),  # 'casa', 'trabajo', 'otro'
    Column("calle", String(100), nullable=False),
    Column("numero", String(10)),
    Column("ciudad", String(50), nullable=False),
    Column("codigo_postal", String(10)),
    Column("pais", String(50), default="Costa Rica"),
    Column("direccion_principal", Boolean, default=False),
    Column("fecha_creacion", DateTime, default=func.now())
)

# ==========================================
# TABLA AUTOMÓVILES (FK opcional a usuarios)
# ==========================================
automoviles_table = Table(
    "automoviles",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=True),  # FK OPCIONAL
    Column("marca", String(30), nullable=False),
    Column("modelo", String(50), nullable=False),
    Column("año", Integer, nullable=False),
    Column("color", String(20)),
    Column("placa", String(20), unique=True),
    Column("numero_chasis", String(50), unique=True),
    Column("precio", Numeric(10, 2)),  # Para precios con decimales
    Column("disponible", Boolean, default=True),  # Si está disponible para asignar
    Column("fecha_registro", DateTime, default=func.now()),
    Column("observaciones", Text)
)

def create_database_schema(database_uri="sqlite:///ejercicio2_orm.db"):
    """
    Crea todas las tablas en la base de datos especificada
    """
    print("=" * 60)
    print("CREANDO ESQUEMA DE BASE DE DATOS")
    print("=" * 60)
    
    # Crear engine
    engine = create_engine(database_uri, echo=True)
    
    try:
        # Crear todas las tablas
        metadata_obj.create_all(engine)
        print("\n✅ Todas las tablas creadas exitosamente!")
        
        # Mostrar información de las tablas
        print("\n📋 TABLAS CREADAS:")
        for table_name in metadata_obj.tables.keys():
            table = metadata_obj.tables[table_name]
            print(f"\n🔹 Tabla: {table_name}")
            print("   Columnas:")
            for column in table.columns:
                nullable = "NULL" if column.nullable else "NOT NULL"
                pk = " (PK)" if column.primary_key else ""
                fk = f" (FK → {list(column.foreign_keys)[0].target_fullname})" if column.foreign_keys else ""
                print(f"     - {column.name}: {column.type} {nullable}{pk}{fk}")
                
        return engine
        
    except Exception as e:
        print(f"❌ Error creando esquema: {e}")
        return None

def show_table_relationships():
    """
    Muestra las relaciones entre tablas de manera clara
    """
    print("\n" + "=" * 60)
    print("RELACIONES ENTRE TABLAS")
    print("=" * 60)
    
    print("\n🔗 RELACIONES DEFINIDAS:")
    print("\n1️⃣  USUARIOS (1) ←→ (N) DIRECCIONES")
    print("    - Relación: Uno a Muchos")
    print("    - FK: direcciones.usuario_id → usuarios.id")
    print("    - Restricción: nullable=False (OBLIGATORIA)")
    print("    - Significado: Cada dirección DEBE pertenecer a un usuario")
    
    print("\n2️⃣  USUARIOS (1) ←→ (N) AUTOMÓVILES")
    print("    - Relación: Uno a Muchos")
    print("    - FK: automoviles.usuario_id → usuarios.id")
    print("    - Restricción: nullable=True (OPCIONAL)")
    print("    - Significado: Los automóviles pueden existir sin propietario asignado")

def demonstrate_schema():
    """
    Función principal que demuestra el esquema completo
    """
    print("🚀 EJERCICIO 2: DISEÑO DE BASE DE DATOS CON SQLAlchemy")
    print("📊 Creando esquema para: usuarios, direcciones y automóviles")
    
    # Crear esquema
    engine = create_database_schema()
    
    if engine:
        # Mostrar relaciones
        show_table_relationships()
        
        print("\n" + "=" * 60)
        print("✅ ESQUEMA COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📝 RESUMEN DEL DISEÑO:")
        print("   • 3 tablas creadas con sus respectivas restricciones")
        print("   • Foreign Keys configuradas según requerimientos")
        print("   • Direcciones: FK obligatoria a usuarios")
        print("   • Automóviles: FK opcional a usuarios")
        print("   • Listo para insertar datos en el próximo ejercicio")
        
        return engine
    else:
        print("❌ No se pudo crear el esquema")
        return None

if __name__ == "__main__":
    # Ejecutar demostración
    engine = demonstrate_schema()
    
