-- Supabase Schema for Cabana Nuwara Eliya

-- 1. Rooms Table
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    image VARCHAR(255),
    capacity INTEGER NOT NULL,
    amenities JSONB
);

-- 2. Testimonials Table
CREATE TABLE testimonials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    text TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5)
);

-- 3. Amenities Table
CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    icon VARCHAR(50),
    title VARCHAR(255) NOT NULL,
    "desc" TEXT
);

-- 4. Bookings Table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    cabana_id INTEGER REFERENCES rooms(id),
    checkin DATE NOT NULL,
    checkout DATE NOT NULL,
    checkin_time TIME,
    checkout_time TIME,
    guests INTEGER NOT NULL,
    days_spent INTEGER,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Contacts Table
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    fname VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Data

-- Rooms Seed Data
INSERT INTO rooms (id, name, description, price, image, capacity, amenities) VALUES
(1, 'Main Cabana (Eury Nature Cabana)', 'Our spacious signature cabana, offering ample room with 3 comfortable triple beds. Perfect for larger groups or families.', 25000, 'room4.jpg', 9, '["3x Triple Beds", "Garden View", "Private Deck", "TV Support", "Carrom & Chess"]'),
(2, 'Little Eury Nature Cabana', 'A private, charming sanctuary. Featuring 2 comfortable double beds and stunning views of the surrounding misty hills.', 15000, 'room2.jpg', 4, '["2x Double Beds", "Veranda", "Mountain View", "TV Support", "Hot Water"]');

-- Adjust the sequence for rooms
SELECT setval('rooms_id_seq', (SELECT MAX(id) FROM rooms));

-- Testimonials Seed Data
INSERT INTO testimonials (name, location, text, rating) VALUES
('Ashan & Dilini', 'Colombo, Sri Lanka', 'An absolutely magical stay! The misty mornings, the cozy private veranda, and the warm Ceylon tea made our anniversary unforgettable. Eury Nature Cabana exceeded every expectation.', 5),
('James & Sarah', 'London, UK', 'The most charming wooden cabanas we''ve stayed at in Sri Lanka. The mountain views are spectacular, the space is beautifully cozy, and the staff is extremely hospitable. We''ll be back!', 5),
('Priya & Family', 'Bangalore, India', 'Perfect highland escape for the family. The kids loved the tea gardens and we loved the cozy family cabana. The hospitality was exceptional!', 5);

-- Amenities Seed Data
INSERT INTO amenities (icon, title, "desc") VALUES
('🎮', 'Indoor Games', 'Enjoy Carrom, Chess, and Card Games during your stay'),
('🔥', 'BBQ Facilities', 'Outdoor BBQ setup for memorable evening dinners'),
('📺', 'TV Support', 'Entertainment available with TV support in cabanas'),
('🚗', 'Parking Space', 'Secure parking space available for guests'),
('🌐', 'High-Speed Wi-Fi', 'Stay connected with high-speed internet throughout your stay'),
('🌅', 'Panoramic Viewing Deck', 'Take in the stunning misty mountain sunrises and peaceful evening views');

-- 6. Menu Items Table
CREATE TABLE IF NOT EXISTS menu_items (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Menu Items
INSERT INTO menu_items (category, name, description, price) VALUES
('breakfast', 'Rice & Curry', 'Red or White Rice Dhal Curry, Pol Sambol, Chicken Curry', 'Rs.600.00'),
('breakfast', 'String Hoppers', '10 String Hoppers, Dhal or Egg Curry, Pol Sambol', 'Rs.550.00'),
('lunch', 'Set Menu', 'Sliced Fried Rice, Devilled Chicken, Chicken Curry, Fresh Salad, Papadam, & Dessert', 'Rs.1,000.00'),
('dinner', 'Chicken Fried Rice', '', 'Rs.950.00'),
('dinner', 'Egg Fried Rice', '', 'Rs.950.00'),
('dinner', 'Chicken Noodles', '', 'Rs.950.00'),
('dinner', 'Egg Noodles', '', 'Rs.900.00'),
('dinner', 'Chicken Kottu', '', 'Rs.950.00'),
('dinner', 'Egg Kottu', '', 'Rs.950.00'),
('dinner', 'Devilled Chicken (Spicy)', '', 'Rs.1,500.00'),
('dinner', 'Egg Omelette', '', 'Rs.550.00');

-- 7. Gallery Items Table
CREATE TABLE IF NOT EXISTS gallery_items (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL,
    caption VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO gallery_items (url, caption, category) VALUES
('static/images/cabana_interior_1.jpg', 'Grand Family Cabana Room', 'cabanas'),
('static/images/cabana_interior_2.jpg', 'Main Cabana Kitchen Area', 'cabanas'),
('static/images/sunrise.jpg', 'Misty Mountain Sunrise', 'views'),
('static/images/cabana_interior_5.jpg', 'Cozy Cabana Living Lounge', 'cabanas'),
('static/images/cabanas_landscape.jpg', 'Eury Nature Cabana Landscape', 'views'),
('static/images/cabana_interior_6.jpg', 'Little Eury Cozy Bedroom', 'cabanas'),
('static/images/cabana_view_balcony.jpg', 'Misty Highland Balcony View', 'views'),
('static/images/dining_1.jpg', 'Cozy Dining Setup', 'dining'),
('static/images/cabana_interior_3.jpg', 'Ceylon Tea close-up', 'dining'),
('static/images/fields_terraced.jpg', 'Terraced Green Fields', 'gardens'),
('static/images/little_eury_exterior.jpg', 'Little Eury Picnic Area', 'gardens'),
('static/images/cabana_view_patio.jpg', 'Panoramic Patio Overlook', 'views'),
('static/images/cabana_picnic_table.jpg', 'Cozy A-frame picnic seating area', 'cabanas'),
('static/images/fields_and_misty_mountains.jpg', 'Panoramic view of agricultural terraced fields and mountains', 'views'),
('static/images/eury_nature_cabana_signboard.jpg', 'Eury Nature Cabana welcome signboard', 'views'),
('static/images/barbecue_chicken_grill.jpg', 'Sizzling evening barbecue grill', 'dining'),
('static/images/scenic_highland_fields.jpg', 'Scenic terraced fields and pine forests', 'views'),
('static/videos/cabana_tour_1.mp4', 'Highland Mist Tour', 'videos'),
('static/videos/cabana_tour_2.mp4', 'Cabana & Garden Walk', 'videos');

