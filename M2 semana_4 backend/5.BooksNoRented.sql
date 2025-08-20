-- SQLite # Obtenga todos los libros que no han sido rentados
SELECT 
  b.ID   AS BookID,
  b.Name AS Book
FROM Books b
LEFT JOIN Rents r 
  ON r.BookID = b.ID
WHERE r.ID IS NULL
ORDER BY b.ID;
