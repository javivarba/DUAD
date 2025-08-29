# src/app.py
from flask import Flask, request, jsonify
from src.repositories.user_repository import UserRepository
from src.repositories.automobile_repository import AutomobileRepository
from src.repositories.rental_repository import RentalRepository

app = Flask(__name__)

def parse_bool(v):
    if isinstance(v, bool):
        return v
    s = str(v or "").strip().lower()
    return s in ("true","1","yes","y","si","sí")

# Cambiar estado de un automovil
@app.patch("/api/automobiles/<int:car_id>/status")
def change_car_status(car_id):
    data = request.get_json(force=True)
    status = data.get("status") or data.get("estado")
    if not status:
        return jsonify(error="Faltan campos: status/estado"), 400
    try:
        car = AutomobileRepository.set_status(car_id, status)
        return jsonify(car), 200
    except ValueError as e:
        msg = str(e)
        if msg == "CAR_NOT_FOUND":
            return jsonify(error=msg), 404
        if msg in ("CAR_STATUS_INVALID","CAR_HAS_OPEN_RENTAL"):
            return jsonify(error=msg), 409
        return jsonify(error="INTERNAL_ERROR"), 500

# Cambiar estado de un usuario (activo/inactivo)
@app.patch("/api/users/<int:user_id>/status")
def change_user_status(user_id):
    data = request.get_json(silent=True) or {}
    if "active" not in data:
        return jsonify(error="Falta campo: active (true/false)"), 400
    try:
        row = UserRepository.set_status(user_id, parse_bool(data["active"]))
        return jsonify(row), 200
    except ValueError as e:
        if str(e) == "USER_NOT_FOUND":
            return jsonify(error="USER_NOT_FOUND"), 404
        return jsonify(error=f"INTERNAL_ERROR: {e!s}"), 500
    except psycopg.Error as e:
        # Muestra el mensaje nativo de Postgres para identificar la columna exacta
        return jsonify(error=f"PG_ERROR: {getattr(e, 'pgerror', str(e))}"), 500
    except Exception as e:
        return jsonify(error=f"INTERNAL_ERROR: {type(e).__name__}"), 500


#  Completar un alquiler
@app.patch("/api/rentals/<int:rental_id>/complete")
def complete_rental(rental_id):
    try:
        rental = RentalRepository.complete(rental_id)
        return jsonify(rental), 200
    except ValueError as e:
        msg = str(e)
        if msg in ("RENTAL_NOT_FOUND", "CAR_NOT_FOUND"):
            return jsonify(error=msg), 404
        return jsonify(error="INTERNAL_ERROR"), 500

#  Cambiar el estado de un alquiler
@app.patch("/api/rentals/<int:rental_id>/status")
def change_rental_status(rental_id):
    data = request.get_json(force=True)
    status = data.get("status") or data.get("estado")
    if not status:
        return jsonify(error="Faltan campos: status/estado"), 400
    try:
        rental = RentalRepository.set_status(rental_id, status)
        return jsonify(rental), 200
    except ValueError as e:
        msg = str(e)
        if msg in ("RENTAL_NOT_FOUND","CAR_NOT_FOUND"):
            return jsonify(error=msg), 404
        if msg in ("RENTAL_STATUS_INVALID","CAR_NOT_AVAILABLE"):
            return jsonify(error=msg), 409
        return jsonify(error="INTERNAL_ERROR"), 500

# Flagear usuario como moroso / no moroso
@app.patch("/api/users/<int:user_id>/delinquent")
def flag_user_delinquent(user_id):
    data = request.get_json(force=True)
    flag = data.get("delinquent", data.get("moroso"))
    if flag is None:
        return jsonify(error="Falta campo: delinquent/moroso (true/false)"), 400

    try:
        row = UserRepository.set_delinquent(user_id, parse_bool(flag))
        return jsonify(row), 200
    except ValueError as e:
        if str(e) == "USER_NOT_FOUND":
            return jsonify(error="USER_NOT_FOUND"), 404
        return jsonify(error="INTERNAL_ERROR"), 500
    except Exception as e:
        return jsonify(error=f"INTERNAL_ERROR: {type(e).__name__}"), 500
    
def _get_pagination():
    try:
        limit  = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        limit, offset = 100, 0
    limit  = max(1, min(limit, 500))  # acota por seguridad
    offset = max(0, offset)
    return limit, offset

@app.get("/api/users")
def list_users():
    limit, offset = _get_pagination()
    username = request.args.get("username")
    rows = UserRepository.list_all(username=username, limit=limit, offset=offset)
    return jsonify(rows), 200

@app.get("/api/automobiles")
def list_automobiles():
    limit, offset = _get_pagination()
    # aceptar 'model' o 'modelo' como sinónimos
    model = request.args.get("model") or request.args.get("modelo")
    status = request.args.get("status") or request.args.get("estado")
    try:
        rows = AutomobileRepository.list_all(model=model, status=status, limit=limit, offset=offset)
        return jsonify(rows), 200
    except ValueError as e:
        if str(e) == "INVALID_CAR_STATUS":
            return jsonify(error="INVALID_CAR_STATUS"), 400
        return jsonify(error=f"INTERNAL_ERROR: {type(e).__name__}"), 500

@app.get("/api/rentals")
def list_rentals():
    limit, offset = _get_pagination()
    status  = request.args.get("status") or request.args.get("estado")
    user_id = request.args.get("user_id")
    car_id  = request.args.get("car_id")
    try:
        rows = RentalRepository.list_all(
            status=status,
            user_id=int(user_id) if user_id else None,
            car_id=int(car_id) if car_id else None,
            limit=limit,
            offset=offset,
        )
        return jsonify(rows), 200
    except ValueError as e:
        if str(e) == "INVALID_RENTAL_STATUS":
            return jsonify(error="INVALID_RENTAL_STATUS"), 400
        return jsonify(error=f"INTERNAL_ERROR: {type(e).__name__}"), 500


@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    print(">>> Flask iniciando en http://127.0.0.1:5000 …")
    app.run(host="127.0.0.1", port=5000, debug=True)
