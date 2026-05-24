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
(1, 'Main Cabana (Eury Nature Cabana)', 'Our spacious signature cabana, offering ample room with 3 comfortable triple beds. Perfect for larger groups or families.', 25000, 'room4.jpg', 9, '["3x Triple Beds", "Garden View", "Private Deck", "Free Wi-Fi", "TV Support", "Carrom & Chess"]'),
(2, 'Little Eury Nature Cabana', 'A private, charming sanctuary. Featuring 2 comfortable double beds and stunning views of the surrounding misty hills.', 15000, 'room2.jpg', 4, '["2x Double Beds", "Veranda", "Mountain View", "Free Wi-Fi", "TV Support", "Hot Water"]');

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
