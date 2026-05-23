from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Hotel data
ROOMS = [
    {
        "id": 1,
        "name": "Grand Family Cabana (Big)",
        "description": "Our spacious signature family cabana, nestled in the peaceful tea gardens of Nuwara Eliya. Featuring two queen beds, a private viewing deck, and ample room for the family to relax.",
        "price": 25000,
        "image": "room4.jpg",
        "capacity": 4,
        "amenities": ["2 Queen Beds", "Garden View", "Private Deck", "Free Wi-Fi", "Tea Maker", "Cozy Fireplace"]
    },
    {
        "id": 2,
        "name": "Classic Cozy Cabana I (Small)",
        "description": "A private, charming sanctuary designed for couples. Featuring a comfortable king-size bed, private veranda, and stunning views of the surrounding misty hills.",
        "price": 15000,
        "image": "room2.jpg",
        "capacity": 2,
        "amenities": ["1 King Bed", "Veranda", "Mountain View", "Free Wi-Fi", "Tea Maker", "Hot Water"]
    },
    {
        "id": 3,
        "name": "Classic Cozy Cabana II (Small)",
        "description": "An elegant, cozy retreat offering comfort and privacy. Perfectly suited for couples or solo travelers wishing to experience the misty mornings of Nuwara Eliya.",
        "price": 15000,
        "image": "room3.jpg",
        "capacity": 2,
        "amenities": ["1 King Bed", "Veranda", "Garden View", "Free Wi-Fi", "Tea Maker", "Hot Water"]
    }
]

TESTIMONIALS = [
    {
        "name": "Ashan & Dilini",
        "location": "Colombo, Sri Lanka",
        "text": "An absolutely magical stay! The misty mornings, the cozy private veranda, and the warm Ceylon tea made our anniversary unforgettable. Cabana Nuwara Eliya exceeded every expectation.",
        "rating": 5
    },
    {
        "name": "James & Sarah",
        "location": "London, UK",
        "text": "The most charming wooden cabanas we've stayed at in Sri Lanka. The mountain views are spectacular, the space is beautifully cozy, and the staff is extremely hospitable. We'll be back!",
        "rating": 5
    },
    {
        "name": "Priya & Family",
        "location": "Bangalore, India",
        "text": "Perfect highland escape for the family. The kids loved the tea gardens and we loved the cozy family cabana. The hospitality was exceptional!",
        "rating": 5
    }
]

AMENITIES = [
    {"icon": "🍃", "title": "Tea Garden Tours", "desc": "Guided tours through pristine tea plantations right at your doorstep"},
    {"icon": "🔥", "title": "Cozy Fire Pit", "desc": "Warm up by our outdoor fire pit under the starry highland sky"},
    {"icon": "☕", "title": "Fresh Ceylon Tea", "desc": "Complimentary freshly brewed Ceylon tea served daily to your cabana"},
    {"icon": "🌿", "title": "Garden & Courtyard", "desc": "Lushly landscaped gardens perfect for morning strolls and photography"},
    {"icon": "🌐", "title": "High-Speed Wi-Fi", "desc": "Stay connected with high-speed internet throughout your stay"},
    {"icon": "🌅", "title": "Panoramic Viewing Deck", "desc": "Take in the stunning misty mountain sunrises and peaceful evening views"},
]

@app.route('/')
def index():
    return render_template('index.html', rooms=ROOMS, testimonials=TESTIMONIALS, amenities=AMENITIES)

@app.route('/accommodations')
def accommodations():
    return render_template('accommodations.html', rooms=ROOMS)

@app.route('/amenities')
def amenities():
    return render_template('amenities.html', amenities=AMENITIES)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return jsonify({"success": True, "message": "Thank you! We'll be in touch shortly."})
    return render_template('contact.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        data = request.json or request.form
        cabana_id = int(data.get('cabana_id', 1))
        checkin_date = data.get('checkin')
        checkout_date = data.get('checkout')
        checkin_time = data.get('checkin_time')
        checkout_time = data.get('checkout_time')
        guests = data.get('guests')
        days_spent = data.get('days_spent')
        
        selected_cabana = next((r for r in ROOMS if r["id"] == cabana_id), ROOMS[0])
        
        # Real-time booking logic simulations
        return jsonify({
            "success": True,
            "message": f"Successfully reserved {selected_cabana['name']} for {days_spent} nights ({checkin_date} to {checkout_date}). We look forward to welcoming you!"
        })
    return render_template('book.html', rooms=ROOMS)

@app.route('/api/rooms')
def api_rooms():
    return jsonify(ROOMS)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
