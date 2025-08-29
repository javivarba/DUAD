# src/repositories/rental_repository.py
from typing import Dict, Any, List, Optional
from src.db import get_cursor
from psycopg import errors

SCHEMA = "lyfter_car_rental"
TABLE_RENTALS = "rentals"

RENTAL_STATUS_MAP = {
    "ongoing": "ongoing",     "en_curso": "ongoing",
    "completed": "completed", "completado": "completed",
    "cancelled": "cancelled", "cancelado": "cancelled",
}

def _is_user_active(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() == "active"

def _is_car_available(v: Any) -> bool:
    s = str(v or "").strip().lower()
    return s in ("available", "disponible")

def _to_rented() -> str:
    return "rented"

def _to_available() -> str:
    return "available"

def _norm_rental_status(s: str) -> str:
    s = (s or "").strip().lower()
    mapa = {
        "ongoing": "ongoing", "en_curso": "ongoing", "en curso": "ongoing",
        "completed": "completed", "completado": "completed", "finalizado": "completed",
        "cancelled": "cancelled", "cancelado": "cancelled"
    }
    if s not in mapa:
        raise ValueError("RENTAL_STATUS_INVALID")
    return mapa[s]

class RentalRepository:
    @staticmethod
    def create(user_id: int, automobile_id: int) -> Dict:
        with get_cursor() as cur:
            cur.execute(
                f"SELECT estado_cuenta, COALESCE(moroso,false) AS moroso FROM {SCHEMA}.users WHERE id = %s FOR UPDATE",
                (user_id,),
            )
            u = cur.fetchone()
            if not u:
                raise ValueError("USER_NOT_FOUND")
            if not _is_user_active(u["estado_cuenta"]):
                raise ValueError("USER_NOT_ACTIVE")
            if bool(u["moroso"]):
                raise ValueError("USER_DELINQUENT")

            cur.execute(
                f"SELECT estado_automovil FROM {SCHEMA}.cars WHERE id = %s FOR UPDATE",
                (automobile_id,),
            )
            c = cur.fetchone()
            if not c:
                raise ValueError("CAR_NOT_FOUND")
            if not _is_car_available(c["estado_automovil"]):
                raise ValueError("CAR_NOT_AVAILABLE")

            cur.execute(
                f"""
                SELECT EXISTS(
                  SELECT 1 FROM {SCHEMA}.rentals
                  WHERE car_id = %s
                    AND trim(lower(estado_alquiler)) IN ('ongoing','en_curso')
                ) AS has_open;
                """,
                (automobile_id,),
            )
            if cur.fetchone()["has_open"]:
                raise ValueError("CAR_NOT_AVAILABLE")

            try:
                cur.execute(
                    f"""
                    INSERT INTO {SCHEMA}.rentals (user_id, car_id, estado_alquiler)
                    VALUES (%s, %s, %s)
                    RETURNING id, user_id, car_id, fecha_alquiler, estado_alquiler;
                    """,
                    (user_id, automobile_id, "ongoing"),
                )
                rental = cur.fetchone()
            except errors.UniqueViolation:
                raise ValueError("CAR_NOT_AVAILABLE")
            except errors.ForeignKeyViolation:
                raise ValueError("USER_NOT_FOUND_OR_CAR_NOT_FOUND")

            cur.execute(
                f"UPDATE {SCHEMA}.cars SET estado_automovil = %s WHERE id = %s",
                (_to_rented(), automobile_id),
            )
            return rental

    @staticmethod
    def complete(rental_id: int) -> Dict:
        with get_cursor() as cur:
            # renta + coche (lock)
            cur.execute(
                f"""
                SELECT r.id, r.car_id, r.estado_alquiler
                FROM {SCHEMA}.rentals r
                WHERE r.id = %s
                FOR UPDATE;
                """,
                (rental_id,),
            )
            r = cur.fetchone()
            if not r:
                raise ValueError("RENTAL_NOT_FOUND")
            if r["estado_alquiler"].strip().lower() in ("completed", "completado"):
                # idempotente
                pass
            else:
                # cerrar rental
                cur.execute(
                    f"""
                    UPDATE {SCHEMA}.rentals
                    SET estado_alquiler = 'completed', fecha_devolucion = COALESCE(fecha_devolucion, NOW())
                    WHERE id = %s
                    RETURNING id, user_id, car_id, fecha_alquiler, fecha_devolucion, estado_alquiler;
                    """,
                    (rental_id,),
                )
                # liberar coche
                cur.execute(
                    f"UPDATE {SCHEMA}.cars SET estado_automovil = %s WHERE id = %s",
                    (_to_available(), r["car_id"]),
                )
            # devuelve estado actual
            cur.execute(
                f"""
                SELECT id, user_id, car_id, fecha_alquiler, fecha_devolucion, estado_alquiler
                FROM {SCHEMA}.rentals WHERE id = %s;
                """,
                (rental_id,),
            )
            return cur.fetchone()

    @staticmethod
    def set_status(rental_id: int, status: str) -> Dict:
        target = _norm_rental_status(status)
        with get_cursor() as cur:
            # renta actual
            cur.execute(
                f"SELECT id, user_id, car_id, estado_alquiler FROM {SCHEMA}.rentals WHERE id = %s FOR UPDATE",
                (rental_id,),
            )
            r = cur.fetchone()
            if not r:
                raise ValueError("RENTAL_NOT_FOUND")

            cur_status = str(r["estado_alquiler"] or "").strip().lower()

            if target == "ongoing":
                # requiere coche disponible y sin otro alquiler abierto
                cur.execute(
                    f"SELECT estado_automovil FROM {SCHEMA}.cars WHERE id = %s FOR UPDATE",
                    (r["car_id"],),
                )
                c = cur.fetchone()
                if not c:
                    raise ValueError("CAR_NOT_FOUND")
                if not _is_car_available(c["estado_automovil"]):
                    raise ValueError("CAR_NOT_AVAILABLE")
                cur.execute(
                    f"""
                    SELECT EXISTS(
                      SELECT 1 FROM {SCHEMA}.rentals
                      WHERE car_id = %s
                        AND id <> %s
                        AND trim(lower(estado_alquiler)) IN ('ongoing','en_curso')
                    ) AS has_open;
                    """,
                    (r["car_id"], rental_id),
                )
                if cur.fetchone()["has_open"]:
                    raise ValueError("CAR_NOT_AVAILABLE")
                cur.execute(
                    f"""
                    UPDATE {SCHEMA}.rentals
                    SET estado_alquiler = 'ongoing', fecha_devolucion = NULL
                    WHERE id = %s
                    RETURNING id, user_id, car_id, fecha_alquiler, fecha_devolucion, estado_alquiler;
                    """,
                    (rental_id,),
                )
                cur.execute(
                    f"UPDATE {SCHEMA}.cars SET estado_automovil = %s WHERE id = %s",
                    (_to_rented(), r["car_id"]),
                )

            elif target in ("completed", "cancelled"):
                # cerrar/cancelar y liberar coche
                cur.execute(
                    f"""
                    UPDATE {SCHEMA}.rentals
                    SET estado_alquiler = %s,
                        fecha_devolucion = COALESCE(fecha_devolucion, NOW())
                    WHERE id = %s
                    RETURNING id, user_id, car_id, fecha_alquiler, fecha_devolucion, estado_alquiler;
                    """,
                    (target, rental_id),
                )
                cur.execute(
                    f"UPDATE {SCHEMA}.cars SET estado_automovil = %s WHERE id = %s",
                    (_to_available(), r["car_id"]),
                )
            else:
                raise ValueError("RENTAL_STATUS_INVALID")

            cur.execute(
                f"SELECT id, user_id, car_id, fecha_alquiler, fecha_devolucion, estado_alquiler FROM {SCHEMA}.rentals WHERE id = %s",
                (rental_id,),
            )
            return cur.fetchone()
    @staticmethod
    def list_all(status: Optional[str] = None,
                 user_id: Optional[int] = None,
                 car_id: Optional[int] = None,
                 limit: int = 100,
                 offset: int = 0) -> List[Dict]:
        """
        Lista alquileres. Filtros opcionales:
          - status (mapea español/inglés)
          - user_id
          - car_id
        """
        sql = f"""
            SELECT
                r.id,
                r.user_id,
                r.car_id,
                r.estado_alquiler AS status,
                r.fecha_alquiler,
                r.fecha_devolucion
            FROM {SCHEMA}.{TABLE_RENTALS} r
            WHERE 1=1
        """
        params = []

        if status:
            norm = RENTAL_STATUS_MAP.get(status.strip().lower())
            if not norm:
                raise ValueError("INVALID_RENTAL_STATUS")
            sql += " AND r.estado_alquiler = %s"
            params.append(norm)

        if user_id is not None:
            sql += " AND r.user_id = %s"
            params.append(int(user_id))

        if car_id is not None:
            sql += " AND r.car_id = %s"
            params.append(int(car_id))

        sql += " ORDER BY r.id DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        with get_cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()