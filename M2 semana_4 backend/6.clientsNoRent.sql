-- SQLite # Obtenga todos los clientes que no han rentado ningún libro         
SELECT 
  c.ID   AS CustomerID,
  c.Name AS Customer,
  c.Email
FROM Customers c
LEFT JOIN Rents r 
  ON r.CustomerID = c.ID
WHERE r.ID IS NULL
ORDER BY c.ID;
