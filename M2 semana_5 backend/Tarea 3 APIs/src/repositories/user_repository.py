# src/repositories/user_repository.py
from typing import Dict, List, Optional
from src.db import get_cursor

SCHEMA = "lyfter_car_rental"
TABLE_USERS = "users"

class UserRepository:
    # ... deja tus otros métodos (create, etc.)

    @staticmethod
    def set_status(user_id: int, active: bool) -> Dict:
        """
        Cambia estado_cuenta (BOOLEAN). Devuelve solo columnas 100% seguras.
        """
        sql = f"""
            UPDATE {SCHEMA}.{TABLE}
            SET estado_cuenta = %s
            WHERE id = %s
            RETURNING id, estado_cuenta;        -- <== nada más, evita UndefinedColumn
        """
        with get_cursor() as cur:
            cur.execute(sql, (bool(active), user_id))
            row = cur.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")
            return row
    def set_delinquent(user_id: int, delinquent: bool) -> Dict:
        """
        Actualiza la columna 'moroso' (BOOLEAN) del usuario.
        Retorna columnas seguras para evitar UndefinedColumn.
        Lanza ValueError('USER_NOT_FOUND') si no existe.
        """
        sql = f"""
            UPDATE {SCHEMA}.{TABLE}
            SET moroso = %s
            WHERE id = %s
            RETURNING id, estado_cuenta, moroso;
        """
        with get_cursor() as cur:
            cur.execute(sql, (bool(delinquent), user_id))
            row = cur.fetchone()
            if not row:
                raise ValueError("USER_NOT_FOUND")
            return row
    @staticmethod
    def list_all(username: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Lista usuarios. Filtro opcional por username (ILIKE %username%).
        Soporta paginación por limit/offset.
        """
        sql = f"""
            SELECT
                id,
                full_name,
                email,
                username,
                birth_date,
                estado_cuenta,
                COALESCE(moroso, FALSE) AS moroso,
                COALESCE(created_at, NOW()) AS created_at
            FROM {SCHEMA}.{TABLE_USERS}
            WHERE 1=1
        """
        params = []
        if username:
            sql += " AND username ILIKE %s"
            params.append(f"%{username}%")

        sql += " ORDER BY id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with get_cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()    