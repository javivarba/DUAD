# src/repositories/automobile_repository.py
from typing import Dict, List, Optional
from src.db import get_cursor

SCHEMA = "lyfter_car_rental"
TABLE_CARS = "cars"

CAR_STATUS_MAP = {
    "available": "available", "disponible": "available",
    "rented": "rented",       "alquilado": "rented",
    "maintenance": "maintenance", "mantenimiento": "maintenance",
    "disabled": "disabled",   "deshabilitado": "disabled",
}


def _normalize_car_status(s: str) -> str:
    s = (s or "").strip().lower()
    mapa = {
        "available": "available", "disponible": "available",
        "rented": "rented", "alquilado": "rented",
        "maintenance": "maintenance", "mantenimiento": "maintenance",
        "disabled": "disabled", "deshabilitado": "disabled",
    }
    if s not in mapa:
        raise ValueError("CAR_STATUS_INVALID")
    return mapa[s]

class AutomobileRepository:
    @staticmethod
    def set_status(car_id: int, status: str) -> Dict:
        status_norm = _normalize_car_status(status)
        with get_cursor() as cur:
            # Si se quiere poner en 'available', no debe tener alquiler abierto
            if status_norm == "available":
                cur.execute(
                    f"""
                    SELECT EXISTS(
                      SELECT 1 FROM {SCHEMA}.rentals
                      WHERE car_id = %s
                        AND trim(lower(estado_alquiler)) IN ('ongoing','en_curso')
                    ) AS has_open;
                    """,
                    (car_id,),
                )
                if cur.fetchone()["has_open"]:
                    raise ValueError("CAR_HAS_OPEN_RENTAL")

            cur.execute(
                f"""
                UPDATE {SCHEMA}.cars
                SET estado_automovil = %s
                WHERE id = %s
                RETURNING id, marca, modelo, anio_fabricacion,
                          estado_automovil, COALESCE(fecha_creacion, NOW()) AS created_at;
                """,
                (status_norm, car_id),
            )
            row = cur.fetchone()
            if not row:
                raise ValueError("CAR_NOT_FOUND")
            return row
    @staticmethod
    def list_all(model: Optional[str] = None,
                 status: Optional[str] = None,
                 limit: int = 100,
                 offset: int = 0) -> List[Dict]:
        """
        Lista autos. Filtros opcionales:
          - model (ILIKE %model%)
          - status (mapea español/inglés a estado_automovil)
        """
        sql = f"""
            SELECT
                id,
                marca        AS make,
                modelo       AS model,
                anio_fabricacion AS year_made,
                estado_automovil  AS status,
                COALESCE(fecha_creacion, NOW()) AS created_at
            FROM {SCHEMA}.{TABLE_CARS}
            WHERE 1=1
        """
        params = []

        if model:
            sql += " AND modelo ILIKE %s"
            params.append(f"%{model}%")

        if status:
            norm = CAR_STATUS_MAP.get(status.strip().lower())
            if not norm:
                raise ValueError("INVALID_CAR_STATUS")
            sql += " AND estado_automovil = %s"
            params.append(norm)

        sql += " ORDER BY id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with get_cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
