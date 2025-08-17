-- SQLite
SELECT 
  b.ID   AS BookID,
  b.Name AS Book,
  a.Name AS Author
FROM Books b
LEFT JOIN Authors a 
  ON a.ID = b.Author
ORDER BY b.ID;
