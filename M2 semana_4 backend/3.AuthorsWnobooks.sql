-- SQLite # Obtenga todos los libros que no tienen un autor asociado
SELECT 
  b.ID   AS BookID,
  b.Name AS Book
FROM Books b
LEFT JOIN Authors a 
  ON a.ID = b.Author
WHERE a.ID IS NULL
ORDER BY b.ID;
