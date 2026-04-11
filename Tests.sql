SHOW DATABASES;
USE wichtheory;
SHOW tables;
SELECT COUNT(*) AS total_products FROM products;
INSERT INTO discount_codes (code, discount_percent, active)
VALUES ('WELCOME10', 10.00, TRUE);
SELECT * FROM discount_codes;
