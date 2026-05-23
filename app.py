from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Hotel data
ROOMS = [
    {
        "id": 1,
        "name": "Deluxe Mountain View Room",
        "description": "Wake up to breathtaking misty mountain vistas from your private balcony. Featuring king-size bed, flat screen TV, complimentary Wi-Fi, and all modern amenities.",
        "price": 12500,
        "image": "room1.jpg",
        "capacity": 2,
        "amenities": ["King Bed", "Mountain View", "Balcony", "Free Wi-Fi", "Flat Screen TV", "Mini Bar"]
    },
    {
        "id": 2,
        "name": "Cabana Suite",
        "description": "Our signature suite with a separate living area, kitchenette, and stunning panoramic views of the Nuwara Eliya hills and tea plantations.",
        "price": 19500,
        "image": "room2.jpg",
        "capacity": 2,
        "amenities": ["King Bed", "Kitchenette", "Living Area", "Panoramic View", "Jacuzzi", "Free Wi-Fi"]
    },
    {
        "id": 3,
        "name": "Family Room",
        "description": "Spacious family room with two queen beds, perfect for a family getaway in the cool highlands. Includes a cozy seating area and garden view.",
        "price": 16500,
        "image": "room3.jpg",
        "capacity": 4,
        "amenities": ["Two Queen Beds", "Garden View", "Seating Area", "Free Wi-Fi", "TV", "Safe"]
    },
    {
        "id": 4,
        "name": "Premium Cottage",
        "description": "A private standalone cottage nestled among the tea gardens. Full kitchen, fireplace, and wraparound veranda for the ultimate highland retreat.",
        "price": 28000,
        "image": "room4.jpg",
        "capacity": 4,
        "amenities": ["Full Kitchen", "Fireplace", "Private Veranda", "Garden", "Free Wi-Fi", "Two Bedrooms"]
    }
]

TESTIMONIALS = [
    {
        "name": "Ashan & Dilini",
        "location": "Colombo, Sri Lanka",
        "text": "An absolutely magical stay! The misty mornings, the cozy fireplace, and the impeccable service made our anniversary unforgettable. Cabana Nuwara Eliya exceeded every expectation.",
        "rating": 5
    },
    {
        "name": "James & Sarah",
        "location": "London, UK",
        "text": "The most charming hotel we've stayed at in Sri Lanka. The mountain views are spectacular, the rooms are beautifully appointed, and the staff goes above and beyond. We'll be back!",
        "rating": 5
    },
    {
        "name": "Priya & Family",
        "location": "Bangalore, India",
        "text": "Perfect highland escape for the whole family. The kids loved exploring the tea gardens and we loved the warm hospitality. The food was exceptional — especially the Sri Lankan breakfast!",
        "rating": 5
    }
]

AMENITIES = [
    {"icon": "🏊", "title": "Heated Pool", "desc": "Enjoy our temperature-controlled pool amidst the cool highland air"},
    {"icon": "🍃", "title": "Tea Garden Tours", "desc": "Guided tours through pristine tea plantations right at your doorstep"},
    {"icon": "🔥", "title": "Fireplace Lounge", "desc": "Warm up by our grand fireplace in the colonial-style lounge"},
    {"icon": "🍽️", "title": "Highland Dining", "desc": "Authentic Sri Lankan & international cuisine with mountain views"},
    {"icon": "🧖", "title": "Spa & Wellness", "desc": "Rejuvenating ayurvedic treatments and wellness therapies"},
    {"icon": "☕", "title": "Fresh Ceylon Tea", "desc": "Complimentary freshly brewed Ceylon tea served daily"},
    {"icon": "🚗", "title": "Airport Transfers", "desc": "Comfortable transfers from Colombo, Kandy, and beyond"},
    {"icon": "🌿", "title": "Garden & Courtyard", "desc": "Lushly landscaped gardens perfect for morning strolls"},
]

@app.route('/')
def index():
    return render_template('index.html', rooms=ROOMS[:3], testimonials=TESTIMONIALS, amenities=AMENITIES[:4])

@app.route('/accommodations')
def accommodations():
    return render_template('accommodations.html', rooms=ROOMS)

@app.route('/amenities')
def amenities():
    return render_template('amenities.html', amenities=AMENITIES)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/dining')
def dining():
    return render_template('dining.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        # Here you'd send email / save to DB
        return jsonify({"success": True, "message": "Thank you! We'll be in touch shortly."})
    return render_template('contact.html')

@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    checkin = data.get('checkin')
    checkout = data.get('checkout')
    guests = data.get('guests', 2)
    # In production, this would check availability and create a booking
    return jsonify({
        "success": True,
        "message": f"Availability confirmed for {checkin} to {checkout}. Redirecting to booking...",
        "booking_url": "#"
    })

@app.route('/api/rooms')
def api_rooms():
    return jsonify(ROOMS)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
