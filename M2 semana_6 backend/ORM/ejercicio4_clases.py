#!/usr/bin/env python3
"""
Ejercicio 4: Clases para Manejo de Datos
Sistema completo de CRUD para usuarios, automóviles y direcciones
"""

from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Text,
    ForeignKey, DateTime, Boolean, Numeric, select, insert, update, delete
)
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from typing import List, Dict, Optional, Union

# ==========================================
# DEFINICIÓN DEL ESQUEMA
# ==========================================

def create_schema():
    """Crea y retorna el esquema de la base de datos"""
    metadata = MetaData()
    
    usuarios = Table(
        "usuarios", metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("nombre", String(50), nullable=False),
        Column("apellido", String(50), nullable=False),
        Column("email", String(100), nullable=False, unique=True),
        Column("telefono", String(20)),
        Column("fecha_registro", DateTime, default=func.now()),
        Column("activo", Boolean, default=True)
    )
    
    direcciones = Table(
        "direcciones", metadata,
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
    
    automoviles = Table(
        "automoviles", metadata,
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
    
    return metadata, usuarios, direcciones, automoviles

# ==========================================
# CLASE BASE PARA MANEJO DE DATOS
# ==========================================

class DatabaseManager:
    """Clase base para manejo de conexión a la base de datos"""
    
    def __init__(self, database_uri: str = "sqlite:///ejercicio4_crud.db"):
        self.engine = create_engine(database_uri, echo=False)
        self.metadata, self.usuarios_table, self.direcciones_table, self.automoviles_table = create_schema()
        self._ensure_tables_exist()
    
    def _ensure_tables_exist(self):
        """Asegura que todas las tablas existan"""
        try:
            self.metadata.create_all(self.engine, checkfirst=True)
        except Exception as e:
            print(f"Error creando tablas: {e}")
            raise
    
    def _execute_query(self, query, return_results=True):
        """Ejecuta una query y maneja la transacción"""
        try:
            with self.engine.begin() as conn:  # begin() maneja auto-commit
                result = conn.execute(query)
                if return_results:
                    return result.fetchall()
                return result
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            raise

# ==========================================
# CLASE PARA MANEJO DE USUARIOS
# ==========================================

class UsuarioManager(DatabaseManager):
    """Clase para manejo de operaciones CRUD de usuarios"""
    
    def crear_usuario(self, nombre: str, apellido: str, email: str, telefono: str = None) -> int:
        """Crea un nuevo usuario"""
        try:
            stmt = insert(self.usuarios_table).values(
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono,
                fecha_registro=datetime.now(),
                activo=True
            ).returning(self.usuarios_table.c.id)
            
            result = self._execute_query(stmt)
            user_id = result[0][0]
            print(f"✅ Usuario creado exitosamente con ID: {user_id}")
            return user_id
            
        except IntegrityError:
            print(f"❌ Error: El email '{email}' ya está registrado")
            raise
        except Exception as e:
            print(f"❌ Error creando usuario: {e}")
            raise
    
    def modificar_usuario(self, user_id: int, **campos) -> bool:
        """Modifica un usuario existente"""
        try:
            # Verificar que el usuario existe
            if not self._usuario_existe(user_id):
                print(f"❌ Usuario con ID {user_id} no existe")
                return False
            
            stmt = update(self.usuarios_table).where(
                self.usuarios_table.c.id == user_id
            ).values(**campos)
            
            result = self._execute_query(stmt, return_results=False)
            print(f"✅ Usuario {user_id} modificado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error modificando usuario: {e}")
            return False
    
    def eliminar_usuario(self, user_id: int) -> bool:
        """Elimina un usuario (soft delete - marca como inactivo)"""
        try:
            return self.modificar_usuario(user_id, activo=False)
        except Exception as e:
            print(f"❌ Error eliminando usuario: {e}")
            return False
    
    def consultar_usuarios(self, incluir_inactivos: bool = False) -> List[Dict]:
        """Consulta todos los usuarios"""
        try:
            stmt = select(self.usuarios_table)
            if not incluir_inactivos:
                stmt = stmt.where(self.usuarios_table.c.activo == True)
            
            results = self._execute_query(stmt)
            usuarios = []
            for row in results:
                usuarios.append({
                    'id': row[0], 'nombre': row[1], 'apellido': row[2],
                    'email': row[3], 'telefono': row[4], 'fecha_registro': row[5],
                    'activo': row[6]
                })
            
            print(f"📋 Encontrados {len(usuarios)} usuarios")
            return usuarios
            
        except Exception as e:
            print(f"❌ Error consultando usuarios: {e}")
            return []
    
    def _usuario_existe(self, user_id: int) -> bool:
        """Verifica si un usuario existe"""
        stmt = select(self.usuarios_table.c.id).where(self.usuarios_table.c.id == user_id)
        result = self._execute_query(stmt)
        return len(result) > 0

# ==========================================
# CLASE PARA MANEJO DE AUTOMÓVILES
# ==========================================

class AutomovilManager(DatabaseManager):
    """Clase para manejo de operaciones CRUD de automóviles"""
    
    def crear_automovil(self, marca: str, modelo: str, año: int, color: str = None, 
                       placa: str = None, numero_chasis: str = None, precio: float = None,
                       observaciones: str = None) -> int:
        """Crea un nuevo automóvil"""
        try:
            stmt = insert(self.automoviles_table).values(
                marca=marca, modelo=modelo, año=año, color=color,
                placa=placa, numero_chasis=numero_chasis, precio=precio,
                disponible=True, fecha_registro=datetime.now(),
                observaciones=observaciones
            ).returning(self.automoviles_table.c.id)
            
            result = self._execute_query(stmt)
            auto_id = result[0][0]
            print(f"✅ Automóvil creado exitosamente con ID: {auto_id}")
            return auto_id
            
        except IntegrityError as e:
            if "placa" in str(e):
                print(f"❌ Error: La placa '{placa}' ya está registrada")
            elif "numero_chasis" in str(e):
                print(f"❌ Error: El número de chasis '{numero_chasis}' ya está registrado")
            else:
                print(f"❌ Error de integridad: {e}")
            raise
        except Exception as e:
            print(f"❌ Error creando automóvil: {e}")
            raise
    
    def modificar_automovil(self, auto_id: int, **campos) -> bool:
        """Modifica un automóvil existente"""
        try:
            if not self._automovil_existe(auto_id):
                print(f"❌ Automóvil con ID {auto_id} no existe")
                return False
            
            stmt = update(self.automoviles_table).where(
                self.automoviles_table.c.id == auto_id
            ).values(**campos)
            
            self._execute_query(stmt, return_results=False)
            print(f"✅ Automóvil {auto_id} modificado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error modificando automóvil: {e}")
            return False
    
    def eliminar_automovil(self, auto_id: int) -> bool:
        """Elimina un automóvil (soft delete - marca como no disponible)"""
        try:
            return self.modificar_automovil(auto_id, disponible=False)
        except Exception as e:
            print(f"❌ Error eliminando automóvil: {e}")
            return False
    
    def asociar_automovil_usuario(self, auto_id: int, user_id: int) -> bool:
        """Asocia un automóvil a un usuario"""
        try:
            # Verificar que tanto el auto como el usuario existen
            if not self._automovil_existe(auto_id):
                print(f"❌ Automóvil con ID {auto_id} no existe")
                return False
            
            # Verificar usuario usando UsuarioManager
            usuario_mgr = UsuarioManager()
            if not usuario_mgr._usuario_existe(user_id):
                print(f"❌ Usuario con ID {user_id} no existe")
                return False
            
            # Asociar el automóvil
            return self.modificar_automovil(auto_id, usuario_id=user_id)
            
        except Exception as e:
            print(f"❌ Error asociando automóvil a usuario: {e}")
            return False
    
    def consultar_automoviles(self, incluir_no_disponibles: bool = False) -> List[Dict]:
        """Consulta todos los automóviles"""
        try:
            stmt = select(self.automoviles_table)
            if not incluir_no_disponibles:
                stmt = stmt.where(self.automoviles_table.c.disponible == True)
            
            results = self._execute_query(stmt)
            automoviles = []
            for row in results:
                automoviles.append({
                    'id': row[0], 'usuario_id': row[1], 'marca': row[2],
                    'modelo': row[3], 'año': row[4], 'color': row[5],
                    'placa': row[6], 'numero_chasis': row[7], 'precio': row[8],
                    'disponible': row[9], 'fecha_registro': row[10], 'observaciones': row[11]
                })
            
            print(f"🚗 Encontrados {len(automoviles)} automóviles")
            return automoviles
            
        except Exception as e:
            print(f"❌ Error consultando automóviles: {e}")
            return []
    
    def _automovil_existe(self, auto_id: int) -> bool:
        """Verifica si un automóvil existe"""
        stmt = select(self.automoviles_table.c.id).where(self.automoviles_table.c.id == auto_id)
        result = self._execute_query(stmt)
        return len(result) > 0

# ==========================================
# CLASE PARA MANEJO DE DIRECCIONES
# ==========================================

class DireccionManager(DatabaseManager):
    """Clase para manejo de operaciones CRUD de direcciones"""
    
    def crear_direccion(self, usuario_id: int, tipo_direccion: str, calle: str,
                       ciudad: str, numero: str = None, codigo_postal: str = None,
                       pais: str = "Costa Rica", direccion_principal: bool = False) -> int:
        """Crea una nueva dirección"""
        try:
            # Verificar que el usuario existe
            usuario_mgr = UsuarioManager()
            if not usuario_mgr._usuario_existe(usuario_id):
                print(f"❌ Usuario con ID {usuario_id} no existe")
                raise ValueError(f"Usuario {usuario_id} no existe")
            
            stmt = insert(self.direcciones_table).values(
                usuario_id=usuario_id, tipo_direccion=tipo_direccion,
                calle=calle, numero=numero, ciudad=ciudad,
                codigo_postal=codigo_postal, pais=pais,
                direccion_principal=direccion_principal,
                fecha_creacion=datetime.now()
            ).returning(self.direcciones_table.c.id)
            
            result = self._execute_query(stmt)
            direccion_id = result[0][0]
            print(f"✅ Dirección creada exitosamente con ID: {direccion_id}")
            return direccion_id
            
        except Exception as e:
            print(f"❌ Error creando dirección: {e}")
            raise
    
    def modificar_direccion(self, direccion_id: int, **campos) -> bool:
        """Modifica una dirección existente"""
        try:
            if not self._direccion_existe(direccion_id):
                print(f"❌ Dirección con ID {direccion_id} no existe")
                return False
            
            stmt = update(self.direcciones_table).where(
                self.direcciones_table.c.id == direccion_id
            ).values(**campos)
            
            self._execute_query(stmt, return_results=False)
            print(f"✅ Dirección {direccion_id} modificada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error modificando dirección: {e}")
            return False
    
    def eliminar_direccion(self, direccion_id: int) -> bool:
        """Elimina una dirección (hard delete)"""
        try:
            if not self._direccion_existe(direccion_id):
                print(f"❌ Dirección con ID {direccion_id} no existe")
                return False
            
            stmt = delete(self.direcciones_table).where(
                self.direcciones_table.c.id == direccion_id
            )
            
            self._execute_query(stmt, return_results=False)
            print(f"✅ Dirección {direccion_id} eliminada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error eliminando dirección: {e}")
            return False
    
    def consultar_direcciones(self, usuario_id: int = None) -> List[Dict]:
        """Consulta todas las direcciones o las de un usuario específico"""
        try:
            stmt = select(self.direcciones_table)
            if usuario_id:
                stmt = stmt.where(self.direcciones_table.c.usuario_id == usuario_id)
            
            results = self._execute_query(stmt)
            direcciones = []
            for row in results:
                direcciones.append({
                    'id': row[0], 'usuario_id': row[1], 'tipo_direccion': row[2],
                    'calle': row[3], 'numero': row[4], 'ciudad': row[5],
                    'codigo_postal': row[6], 'pais': row[7], 'direccion_principal': row[8],
                    'fecha_creacion': row[9]
                })
            
            filter_msg = f" para usuario {usuario_id}" if usuario_id else ""
            print(f"🏠 Encontradas {len(direcciones)} direcciones{filter_msg}")
            return direcciones
            
        except Exception as e:
            print(f"❌ Error consultando direcciones: {e}")
            return []
    
    def _direccion_existe(self, direccion_id: int) -> bool:
        """Verifica si una dirección existe"""
        stmt = select(self.direcciones_table.c.id).where(self.direcciones_table.c.id == direccion_id)
        result = self._execute_query(stmt)
        return len(result) > 0

# ==========================================
# FUNCIONES DE DEMOSTRACIÓN
# ==========================================

def demostrar_funcionamiento():
    """Demuestra todas las funcionalidades implementadas"""
    print("🚀 DEMOSTRACIÓN DEL SISTEMA DE MANEJO DE DATOS")
    print("=" * 70)
    
    # Inicializar managers
    usuario_mgr = UsuarioManager()
    auto_mgr = AutomovilManager()
    direccion_mgr = DireccionManager()
    
    try:
        print("\n1️⃣  CREANDO USUARIOS...")
        user1_id = usuario_mgr.crear_usuario("Juan", "Pérez", "juan@email.com", "1234-5678")
        user2_id = usuario_mgr.crear_usuario("María", "González", "maria@email.com", "8765-4321")
        
        print("\n2️⃣  CREANDO AUTOMÓVILES...")
        auto1_id = auto_mgr.crear_automovil("Toyota", "Corolla", 2022, "Blanco", "ABC-123", "TOY123456", 15000.00)
        auto2_id = auto_mgr.crear_automovil("Honda", "Civic", 2021, "Negro", "XYZ-789", "HON789012", 18000.00)
        
        print("\n3️⃣  CREANDO DIRECCIONES...")
        dir1_id = direccion_mgr.crear_direccion(user1_id, "casa", "Calle Principal", "San José", "123", "10001")
        dir2_id = direccion_mgr.crear_direccion(user2_id, "trabajo", "Avenida Central", "Cartago", "456", "30001")
        
        print("\n4️⃣  ASOCIANDO AUTOMÓVIL A USUARIO...")
        auto_mgr.asociar_automovil_usuario(auto1_id, user1_id)
        
        print("\n5️⃣  CONSULTANDO DATOS...")
        usuarios = usuario_mgr.consultar_usuarios()
        automoviles = auto_mgr.consultar_automoviles()
        direcciones = direccion_mgr.consultar_direcciones()
        
        print("\n6️⃣  MODIFICANDO DATOS...")
        usuario_mgr.modificar_usuario(user1_id, telefono="9999-0000")
        auto_mgr.modificar_automovil(auto2_id, color="Azul")
        direccion_mgr.modificar_direccion(dir1_id, numero="123A")
        
        print("\n✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en la demostración: {e}")
        return False

if __name__ == "__main__":
    print("📚 EJERCICIO 4: SISTEMA COMPLETO DE MANEJO DE DATOS")
    print("🎯 Implementación de clases CRUD para usuarios, automóviles y direcciones")
    
    # Ejecutar demostración
    success = demostrar_funcionamiento()
    
    if success:
        print(f"\n🎉 ¡EJERCICIO 4 COMPLETADO EXITOSAMENTE!")
        print(f"💡 Todas las operaciones CRUD están implementadas y funcionando")
    else:
        print(f"\n❌ Hubo errores en la ejecución")