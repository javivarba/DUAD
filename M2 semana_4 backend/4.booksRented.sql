-- SQLite # Obtenga todos los libros que han sido rentados
SELECT DISTINCT 
  b.ID   AS BookID,
  b.Name AS Book
FROM Books b
INNER JOIN Rents r 
  ON r.BookID = b.ID
ORDER BY b.ID;
