# JOINS — Esquema, Datos de ejemplo, Consultas y Capturas

Este README complementa los ejercicios de JOINS. Permite que cualquier revisor cree las tablas **desde cero**, inserte **datos de ejemplo** y ejecute las **consultas** obteniendo los mismos resultados.

---

## ✅ Objetivo

- Proveer **`CREATE TABLE`** y **`INSERT`** para reproducir el entorno.
- Incluir **consultas** por ejercicio (1–7) y **lugares para capturas**.
- Explicar cómo ejecutarlo en **VS Code + SQLite**.

---

## 🗂️ Estructura sugerida

```
M2 semana_4 backend/
├─ README.md  ← este archivo
├─ schema.sql
├─ seed.sql
├─ queries/
│  ├─ 1.allbooks&authors.sql
│  ├─ 2.booksWnoAuthors.sql
│  ├─ 3.AuthorsWnobooks.sql
│  ├─ 4.booksRented.sql
│  ├─ 5.BooksNoRented.sql
│  ├─ 6.clientsNoRent.sql
│  └─ 7.booksoverdue.sql

---

## 1) Esquema — `schema.sql`

Ejecutar este script primero (idempotente):

```sql
PRAGMA foreign_keys = ON;

-- Eliminar tablas si existen (respetando dependencias)
DROP TABLE IF EXISTS rentals;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS clients;

-- Tabla de autores
CREATE TABLE authors (
  id     INTEGER PRIMARY KEY,
  name   TEXT NOT NULL UNIQUE
);

-- Tabla de libros
CREATE TABLE books (
  id         INTEGER PRIMARY KEY,
  title      TEXT NOT NULL,
  author_id  INTEGER NULL,
  FOREIGN KEY (author_id)
    REFERENCES authors(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

-- Tabla de clientes
CREATE TABLE clients (
  id         INTEGER PRIMARY KEY,
  full_name  TEXT NOT NULL,
  email      TEXT UNIQUE
);

-- Tabla de rentas
CREATE TABLE rentals (
  id          INTEGER PRIMARY KEY,
  book_id     INTEGER NOT NULL,
  client_id   INTEGER NOT NULL,
  rented_at   DATE NOT NULL,   -- formato ISO: YYYY-MM-DD
  due_at      DATE NOT NULL,
  returned_at DATE NULL,
  FOREIGN KEY (book_id)  REFERENCES books(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (client_id) REFERENCES clients(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);
```

**Notas del esquema**

- En SQLite no es necesario `AUTOINCREMENT`; `INTEGER PRIMARY KEY` usa `rowid`.
- `PRAGMA foreign_keys = ON;` es clave para forzar integridad referencial.

---

## 2) Datos de ejemplo — `seed.sql`

Datos mínimos para que **todas** las consultas devuelvan filas útiles.

```sql
-- Autores (uno sin libros para el ejercicio 3)
INSERT INTO authors (name) VALUES
  ('Gabriel García Márquez'),  -- id = 1
  ('Jane Austen'),             -- id = 2
  ('Isabel Allende');          -- id = 3  (sin libros)

-- Libros (uno sin autor para el ejercicio 2)
INSERT INTO books (title, author_id) VALUES
  ('Cien años de soledad', 1),
  ('El amor en los tiempos del cólera', 1),
  ('Orgullo y Prejuicio', 2),
  ('Libro huérfano', NULL);

-- Clientes (uno sin rentas para el ejercicio 6)
INSERT INTO clients (full_name, email) VALUES
  ('Carlos Ruiz', 'carlos@example.test'),  -- id = 1
  ('María Fernández', 'maria@example.test'), -- id = 2
  ('Ana Solís', 'ana@example.test');          -- id = 3  (sin rentas)

-- Rentas (una vencida para el ejercicio 7)
INSERT INTO rentals (book_id, client_id, rented_at, due_at, returned_at) VALUES
  (1, 1, '2025-08-01', '2025-08-10', NULL),  -- vencida si hoy > 2025-08-10
  (2, 2, '2025-08-05', '2025-08-25', NULL),  -- activa, no vencida
  (3, 1, '2025-08-10', '2025-08-17', '2025-08-15'); -- ya devuelta
```

---

## 3) Consultas por ejercicio — carpeta `queries/`

> Puedes copiar/pegar cada consulta en su archivo correspondiente para mantener el 1:1 con el enunciado.

### 1. **Todos los libros con su autor** — `1.allbooks&authors.sql`

```sql
SELECT
  b.id,
  b.title,
  a.name AS author_name
FROM books AS b
LEFT JOIN authors AS a
  ON a.id = b.author_id
ORDER BY b.id;
```

### 2. **Libros sin autor** — `2.booksWnoAuthors.sql`

```sql
SELECT b.*
FROM books AS b
WHERE b.author_id IS NULL
ORDER BY b.id;
```

### 3. **Autores sin libros** — `3.AuthorsWnobooks.sql`

```sql
SELECT a.*
FROM authors AS a
LEFT JOIN books AS b
  ON b.author_id = a.id
WHERE b.id IS NULL
ORDER BY a.id;
```

### 4. **Libros actualmente rentados (no devueltos)** — `4.booksRented.sql`

```sql
SELECT
  r.id       AS rental_id,
  b.title    AS book_title,
  c.full_name AS client,
  r.rented_at,
  r.due_at
FROM rentals AS r
JOIN books   AS b ON b.id = r.book_id
JOIN clients AS c ON c.id = r.client_id
WHERE r.returned_at IS NULL
ORDER BY r.rented_at DESC;
```

### 5. **Libros no rentados actualmente** — `5.BooksNoRented.sql`

```sql
SELECT b.*
FROM books AS b
LEFT JOIN rentals AS r
  ON r.book_id = b.id
  AND r.returned_at IS NULL
WHERE r.id IS NULL
ORDER BY b.id;
```

### 6. **Clientes que nunca han rentado** — `6.clientsNoRent.sql`

```sql
SELECT c.*
FROM clients AS c
LEFT JOIN rentals AS r
  ON r.client_id = c.id
WHERE r.id IS NULL
ORDER BY c.id;
```

### 7. **Libros con renta vencida** — `7.booksoverdue.sql`

```sql
SELECT
  b.title    AS book_title,
  c.full_name AS client,
  r.due_at
FROM rentals AS r
JOIN books   AS b ON b.id = r.book_id
JOIN clients AS c ON c.id = r.client_id
WHERE r.returned_at IS NULL
  AND r.due_at < DATE('now')  -- usa UTC
ORDER BY r.due_at ASC;
```

> **Tip:** `DATE('now')` en SQLite usa UTC. Para pruebas con fecha fija puedes reemplazar por `'2025-08-22'`.

---

## 4) ¿Cómo ejecutarlo en VS Code + SQLite?

1. Instala la extensión **SQLite** (AlexCVZZ) o similar.
2. Crea una base `library.db` (clic derecho en el Explorador → *New File*).
3. Abre `schema.sql`, **selecciona todo** y ejecuta (botón ▶ *Run Query*).
4. Abre `seed.sql` y ejecútalo.
5. Abre cada archivo en `queries/` y ejecútalo para obtener resultados.
6. Para reiniciar, vuelve a ejecutar `schema.sql` y `seed.sql` (o borra `library.db`).

> Si usas la CLI de SQLite: `sqlite3 library.db < schema.sql && sqlite3 library.db < seed.sql`.

---

## 5) Notas y limitaciones (SQLite)

- `DATE('now')` usa UTC; si lo prefieres, usa una fecha fija para resultados deterministas.
- Evita `TEXT` con formatos de fecha no ISO; usa `YYYY-MM-DD` para ordenar/filtrar bien.
- `FOREIGN KEY` requiere `PRAGMA foreign_keys = ON;` en cada nueva conexión.

---

##
