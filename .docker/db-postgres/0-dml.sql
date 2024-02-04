CREATE TABLE stock (
  id uuid,
  point_of_sale VARCHAR(6),
  product VARCHAR(63),
  date TIMESTAMP,
  stock float8,
  PRIMARY KEY (id)
);
