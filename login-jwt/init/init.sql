CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Usuario de prueba
INSERT INTO users (email, password_hash)
VALUES (
  'admin@test.com',
  'scrypt:32768:8:1$4DOvPaZgcGS4TwQE$a0823ecdba2079ac85084cf4052d70ec1e0f69693bf3a26e4b69b5ab04943b835aacf9c1e0e6347f12b6bfce03d5215010245a8e0b2147f10b23e24b63a23682'
);
