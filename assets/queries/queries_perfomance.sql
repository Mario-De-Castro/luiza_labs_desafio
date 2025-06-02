EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM clients c WHERE email = 'user@example.com';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM clients c WHERE id = 1;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM wishlist w WHERE client_id = 1;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM wishlist w WHERE product_id = 1;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM wishlist w 
WHERE client_id = 1
AND product_id = 1;
