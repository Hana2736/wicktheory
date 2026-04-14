-- =====================================
-- Wick Theory Candle Store Database
-- =====================================

CREATE DATABASE IF NOT EXISTS wichtheory;
USE wichtheory;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    scent VARCHAR(100),
    size VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    quantity_available INT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Carts Table
CREATE TABLE carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Cart Items Table
CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Orders Table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    total_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    final_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Order Items Table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price_at_purchase DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Discount Codes Table
CREATE TABLE discount_codes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE,
    discount_percent DECIMAL(5,2),
    active BOOLEAN DEFAULT TRUE
);

-- =====================================
-- Insert Products
-- =====================================

-- Scents - citrus, floral, fruity, earthy, gourmet

-- Candles that appear in multiple talbes
-- A Fresh Chapter - L,S
-- Fresh Cut Roses - M,S
-- Juicy Watermelon - L,M

-- Large Candles (L - $29.99)
-- image_url format - candle name all lowercase and no spaces.jpg
INSERT INTO products 
(name, description, scent, size, price, quantity_available, image_url)
VALUES
('A Fresh Chapter', 'Smells like new beginnings', 'citrus', 'L', 29.99, 10, '/images/afreshchapter.jpg'),
('Bahama Breeze', 'Fruity and refreshing', 'fruity', 'L', 29.99, 10, '/images/bahamabreeze.jpg'),
('Chocolate Layer Cake', 'Delicious and indulgent', 'gourmet', 'L', 29.99, 10, '/images/chocolatelayercake.jpg'),
('Clean Cotton', 'Fresh and airy cotton scent', 'earthy', 'L', 29.99, 10, '/images/cleancotton.jpg'),
('Cocoa Dream', 'Rich and velvety chocolate aroma', 'gourmet', 'L', 29.99, 10, '/images/cocoadream.jpg'),
('Coconut Beach', 'Tropical coconut escape', 'fruity', 'L', 29.99, 10, '/images/coconutbeach.jpg'),
('Cucumber Mint Cooler', 'Refreshing cucumber and mint blend', 'earthy', 'L', 29.99, 10, '/images/cucumbermintcooler.jpg'),
('French Vanilla', 'Classic warm vanilla fragrance', 'gourmet', 'L', 29.99, 10, '/images/frenchvanilla.jpg'),
('Juicy Watermelon', 'Sweet and vibrant watermelon scent', 'fruity', 'L', 29.99, 10, '/images/juicywatermelon.jpg'),
('Lemon Blueberry Bliss', 'Bright lemon with sweet blueberry notes', 'fruity', 'L', 29.99, 10, '/images/lemonblueberrybliss.jpg'),
('Lemon Lavender', 'Citrus lemon softened with lavender', 'citrus', 'L', 29.99, 10, '/images/lemonlavender.jpg'),
('Lilac Blossom', 'Soft blooming lilac fragrance', 'floral', 'L', 29.99, 10, '/images/lilacblossom.jpg'),
('Midsummer''s Night', 'Deep and mysterious evening scent', 'earthy', 'L', 29.99, 10, '/images/midsummersnight.jpg'),
('Pink Sands', 'Soft tropical island breeze', 'fruity', 'L', 29.99, 10, '/images/pinksands.jpg'),
('Sage and Citrus', 'Herbal sage with bright citrus notes', 'citrus', 'L', 29.99, 10, '/images/sageandcitrus.jpg'),
('Salted Caramel', 'Sweet caramel with a touch of sea salt', 'gourmet', 'L', 29.99, 10, '/images/saltedcaramel.jpg'),
('Sicilian Lemon', 'Sharp and vibrant lemon zest', 'citrus', 'L', 29.99, 10, '/images/sicilianlemon.jpg'),
('Tangerine and Vanilla', 'Sweet tangerine blended with warm vanilla', 'citrus', 'L', 29.99, 10, '/images/tangerineandvanilla.jpg');

-- Medium Candles (M - $19.99)
-- image_url format - candle name all lowercase and no spaces + 'M'.jpg
INSERT INTO products 
(name, description, scent, size, price, quantity_available, image_url)
VALUES
('Apple Pumpkin', 'Warm apple blended with spiced pumpkin', 'gourmet', 'M', 19.99, 10, '/images/applepumpkinM.jpg'),
('Catching Rays', 'Bright sun-kissed citrus aroma', 'citrus', 'M', 19.99, 10, '/images/catchingraysM.jpg'),
('Fresh Cut Roses', 'Classic blooming rose fragrance', 'floral', 'M', 19.99, 10, '/images/freshcutrosesM.jpg'),
('Green Apple Sorbet', 'Sweet and tart green apple delight', 'fruity', 'M', 19.99, 10, '/images/greenapplesorbetM.jpg'),
('Honey Clementine', 'Golden honey with juicy citrus notes', 'citrus', 'M', 19.99, 10, '/images/honeyclementineM.jpg'),
('Iced Berry Lemonade', 'Chilled berries with zesty lemonade', 'fruity', 'M', 19.99, 10, '/images/icedberrylemonadeM.jpg'),
('Juicy Watermelon', 'Sweet and vibrant watermelon scent', 'fruity', 'M', 19.99, 10, '/images/juicywatermelonM.jpg'),
('Magical Bright Lights', 'Vibrant sparkling festive fragrance', 'floral', 'M', 19.99, 10, '/images/magicalbrightlightsM.jpg'),
('Sparkling Cinnamon', 'Warm cinnamon with a sparkling twist', 'gourmet', 'M', 19.99, 10, '/images/sparklingcinnamonM.jpg'),
('Starfruit & Sunshine', 'Exotic starfruit with bright citrus glow', 'fruity', 'M', 19.99, 10, '/images/starfruitsunshineM.jpg'),
('Vintage Velvet', 'Deep smooth luxurious fragrance', 'earthy', 'M', 19.99, 10, '/images/vintagevelvetM.jpg');

-- Small Candles (S - $9.99)
-- image_url format - candle name all lowercase and no spaces + 'S'.jpg
INSERT INTO products 
(name, description, scent, size, price, quantity_available, image_url)
VALUES
('A Fresh Chapter', 'Smells like new beginnings', 'citrus', 'S', 9.99, 10, '/images/afreshchapterS.jpg'),
('Balsam And Cedar', 'Warm balsam and cedar wood fragrance', 'earthy', 'S', 9.99, 10, '/images/balsamandcedarS.jpg'),
('Fresh Cut Roses', 'Classic blooming rose fragrance', 'floral', 'S', 9.99, 10, '/images/freshcutrosesS.jpg'),
('Serenity Stone', 'Calming mineral and earthy tones', 'earthy', 'S', 9.99, 10, '/images/serenitystoneS.jpg'),
('Slow Bloom', 'Delicate floral aroma unfolding slowly', 'floral', 'S', 9.99, 10, '/images/slowbloomS.jpg'),
('Spring Herbarium', 'Fresh spring herbs and greenery', 'earthy', 'S', 9.99, 10, '/images/springherbariumS.jpg'),
('Wildflower Breeze', 'Light and airy wildflower scent', 'floral', 'S', 9.99, 10, '/images/wildflowerbreezeS.jpg');
