DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS specials;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_price DECIMAL(15, 2) NOT NULL
);

CREATE TABLE specials (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  special_code TEXT NOT NULL,
  special_description TEXT NOT NULL,
  special_limit INTEGER,
  special_discount DECIMAL(15, 2) NOT NULL,
  special_product_code_link TEXT NOT NULL,
  special_discount_rate DECIMAL(15, 2) NOT NULL,
  FOREIGN KEY (special_product_code_link) REFERENCES products (product_code)
);

INSERT INTO products (product_code, product_name, product_price) VALUES ("CH1", "Chai", 3.11);
INSERT INTO products (product_code, product_name, product_price) VALUES ("AP1", "Apples", 6.00);
INSERT INTO products (product_code, product_name, product_price) VALUES ("CF1", "Coffee", 11.23);
INSERT INTO products (product_code, product_name, product_price) VALUES ("MK1", "Milk", 4.75);
INSERT INTO products (product_code, product_name, product_price) VALUES ("OM1", "Oatmeal", 3.69);

INSERT INTO specials (special_code, special_description, special_limit, special_product_code_link, special_discount, special_discount_rate) VALUES ("BOGO", "Buy-One-Get-One-Free Special on Coffee.", NULL, "CF1", 11.23, 1);
INSERT INTO specials (special_code, special_description, special_limit, special_product_code_link, special_discount, special_discount_rate) VALUES ("APPL", "If you buy 3 or more bags of Apples, the price drops to $4.50.", NULL, "AP1", 1.50, .25);
INSERT INTO specials (special_code, special_description, special_limit, special_product_code_link, special_discount, special_discount_rate) VALUES ("CHMK", "Purchase a box of Chai and get milk free.", 1, "CH1", 4.75, 1);
INSERT INTO specials (special_code, special_description, special_limit, special_product_code_link, special_discount, special_discount_rate) VALUES ("APOM", "Purchase a bag of Oatmeal and get 50% off a bag of Apples", NULL, "OM1", 3.00, .50);


