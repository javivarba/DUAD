-- SQLite
SELECT DISTINCT 
  b.ID   AS BookID,
  b.Name AS Book
FROM Books b
INNER JOIN Rents r 
  ON r.BookID = b.ID
WHERE r.State = 'Overdue'
ORDER BY b.ID;
