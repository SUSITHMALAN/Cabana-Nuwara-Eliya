import os
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for the frontend to communicate with the backend
CORS(app, resources={r"/api/*": {"origins": "*"}})

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not configured. Please set it in your .env file.")
    
    # Strip query parameters that psycopg2 does not support (like pgbouncer)
    cleaned_url = DATABASE_URL
    if '?' in cleaned_url:
        cleaned_url = cleaned_url.split('?')[0]
        
    return psycopg2.connect(cleaned_url)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok", "message": "Backend API is running with direct PostgreSQL connection."})

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, name, description, price, image, capacity, amenities FROM rooms ORDER BY id")
        rooms = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rooms)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, name, location, text, rating FROM testimonials")
        testimonials = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(testimonials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/amenities', methods=['GET'])
def get_amenities():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT id, icon, title, "desc" FROM amenities')
        amenities = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(amenities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    required_fields = ['cabana_id', 'checkin', 'checkout', 'guests', 'fname', 'lname', 'email', 'phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    try:
        booking_data = {
            "cabana_id": int(data.get('cabana_id')),
            "checkin": data.get('checkin'),
            "checkout": data.get('checkout'),
            "checkin_time": data.get('checkin_time'),
            "checkout_time": data.get('checkout_time'),
            "guests": int(data.get('guests')),
            "days_spent": int(data.get('days_spent', 1)),
            "fname": data.get('fname'),
            "lname": data.get('lname'),
            "email": data.get('email'),
            "phone": data.get('phone'),
            "notes": data.get('notes'),
            "status": "pending"
        }

        # Date validations: backdate and chronological order check
        from datetime import datetime, date
        try:
            checkin_d = datetime.strptime(booking_data['checkin'], '%Y-%m-%d').date()
            checkout_d = datetime.strptime(booking_data['checkout'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format. Use YYYY-MM-DD."}), 400

        if checkin_d < date.today():
            return jsonify({"success": False, "message": "Check-in date cannot be in the past."}), 400

        if checkout_d <= checkin_d:
            return jsonify({"success": False, "message": "Check-out date must be after check-in date."}), 400
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Overlap Check: any pending/confirmed booking for the same cabana where checkin < checkout_d AND checkout > checkin_d
        cur.execute("""
            SELECT id FROM bookings
            WHERE cabana_id = %s
              AND status != 'cancelled'
              AND checkin < %s
              AND checkout > %s
        """, (booking_data['cabana_id'], booking_data['checkout'], booking_data['checkin']))
        overlap = cur.fetchone()
        if overlap:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "This cabana is already booked for the selected dates. Please choose different dates."}), 400

        cur.execute("""
            INSERT INTO bookings (cabana_id, checkin, checkout, checkin_time, checkout_time, guests, days_spent, fname, lname, email, phone, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            booking_data['cabana_id'], booking_data['checkin'], booking_data['checkout'],
            booking_data['checkin_time'], booking_data['checkout_time'], booking_data['guests'],
            booking_data['days_spent'], booking_data['fname'], booking_data['lname'],
            booking_data['email'], booking_data['phone'], booking_data['notes'], booking_data['status']
        ))
        booking_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        # WhatsApp logic
        admin_number = "94771758395"
        cabana_name = "Main Cabana" if booking_data['cabana_id'] == 1 else "Little Eury Nature Cabana"
        msg = f"Hello Admin! I would like to book {cabana_name} for {booking_data['guests']} guests from {booking_data['checkin']} to {booking_data['checkout']} ({booking_data['days_spent']} nights). My name is {booking_data['fname']} {booking_data['lname']}."
        wa_url = f"https://wa.me/{admin_number}?text={urllib.parse.quote(msg)}"
        
        return jsonify({
            "success": True,
            "message": f"Successfully reserved your cabana for {booking_data['days_spent']} nights. You will now be redirected to WhatsApp to confirm.",
            "whatsapp_url": wa_url
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    required_fields = ['fname', 'lname', 'email', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO contacts (fname, lname, email, phone, subject, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get('fname'), data.get('lname'), data.get('email'),
            data.get('phone'), data.get('subject'), data.get('message')
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "message": "Thank you! We'll be in touch shortly."})
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

# --- Admin Endpoints ---

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    # Hardcoded admin credentials for MVP
    if data.get('username') == 'admin' and data.get('password') == 'euryadmin2024':
        return jsonify({"success": True, "token": "mvp-admin-token-123"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

def check_auth():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != 'Bearer mvp-admin-token-123':
        return False
    return True

@app.route('/api/admin/bookings', methods=['GET'])
def get_bookings():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT b.*, r.name as room_name 
            FROM bookings b
            LEFT JOIN rooms r ON b.cabana_id = r.id
            ORDER BY b.created_at DESC
        """)
        bookings = cur.fetchall()
        cur.close()
        conn.close()
        
        # Format bookings for frontend serialization compatibility
        formatted_bookings = []
        for b in bookings:
            if b.get('created_at'):
                b['created_at'] = b['created_at'].isoformat()
            if b.get('checkin'):
                b['checkin'] = b['checkin'].isoformat()
            if b.get('checkout'):
                b['checkout'] = b['checkout'].isoformat()
            if b.get('checkin_time'):
                b['checkin_time'] = b['checkin_time'].isoformat() if hasattr(b['checkin_time'], 'isoformat') else str(b['checkin_time'])
            if b.get('checkout_time'):
                b['checkout_time'] = b['checkout_time'].isoformat() if hasattr(b['checkout_time'], 'isoformat') else str(b['checkout_time'])
            
            b['rooms'] = {"name": b.get('room_name')}
            formatted_bookings.append(b)
            
        return jsonify(formatted_bookings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/bookings/<int:id>/status', methods=['PUT'])
def update_booking_status(id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    status = data.get('status')
    if not status:
        return jsonify({"error": "Status is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            UPDATE bookings 
            SET status = %s 
            WHERE id = %s 
            RETURNING *
        """, (status, id))
        updated_row = cur.fetchone()
        conn.commit()
        
        if not updated_row:
            cur.close()
            conn.close()
            return jsonify({"error": "Booking not found"}), 404
            
        # Get room name for custom wa message formatting
        cur.execute("SELECT name FROM rooms WHERE id = %s", (updated_row['cabana_id'],))
        room_row = cur.fetchone()
        cur.close()
        conn.close()
        
        # Serialize fields for JSON compatibility
        for key, val in updated_row.items():
            if hasattr(val, 'isoformat'):
                updated_row[key] = val.isoformat()
            elif val is not None and not isinstance(val, (int, float, str, bool, list, dict)):
                updated_row[key] = str(val)

        # If confirmed, generate whatsapp URL for guest
        wa_url = None
        if status == 'confirmed':
            phone = updated_row.get('phone', '')
            formatted_phone = "94" + phone[1:] if phone.startswith('0') else phone
            room_name = room_row['name'] if room_row else "Cabana"
            msg = f"Hello {updated_row.get('fname')}, your booking for {room_name} from {updated_row.get('checkin')} to {updated_row.get('checkout')} is CONFIRMED. Thank you for choosing Eury Nature Cabana!"
            wa_url = f"https://wa.me/{formatted_phone}?text={urllib.parse.quote(msg)}"

        return jsonify({"success": True, "booking": updated_row, "whatsapp_url": wa_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/contacts', methods=['GET'])
def get_contacts():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        contacts = cur.fetchall()
        cur.close()
        conn.close()
        
        for c in contacts:
            if c.get('created_at'):
                c['created_at'] = c['created_at'].isoformat()
                
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Edit Booking Endpoint ---
@app.route('/api/admin/bookings/<int:id>', methods=['PUT'])
def edit_booking(id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get existing booking
        cur.execute("SELECT cabana_id, checkin, checkout FROM bookings WHERE id = %s", (id,))
        existing = cur.fetchone()
        if not existing:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "Booking not found"}), 404
            
        cabana_id = int(data.get('cabana_id', existing['cabana_id']))
        checkin = data.get('checkin', str(existing['checkin']))
        checkout = data.get('checkout', str(existing['checkout']))
        status = data.get('status', 'pending')
        
        # Check overlaps (excluding this booking itself)
        if status != 'cancelled':
            cur.execute("""
                SELECT id FROM bookings
                WHERE cabana_id = %s
                  AND id != %s
                  AND status != 'cancelled'
                  AND checkin < %s
                  AND checkout > %s
            """, (cabana_id, id, checkout, checkin))
            overlap = cur.fetchone()
            if overlap:
                cur.close()
                conn.close()
                return jsonify({"success": False, "message": "The selected dates overlap with an existing booking."}), 400

        cur.execute("""
            UPDATE bookings
            SET cabana_id = %s, checkin = %s, checkout = %s, checkin_time = %s, checkout_time = %s,
                guests = %s, fname = %s, lname = %s, email = %s, phone = %s, notes = %s, status = %s
            WHERE id = %s
            RETURNING *
        """, (
            cabana_id, checkin, checkout, data.get('checkin_time'), data.get('checkout_time'),
            int(data.get('guests')), data.get('fname'), data.get('lname'),
            data.get('email'), data.get('phone'), data.get('notes'), status, id
        ))
        updated_row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Serialize fields for JSON compatibility
        for key, val in updated_row.items():
            if hasattr(val, 'isoformat'):
                updated_row[key] = val.isoformat()
            elif val is not None and not isinstance(val, (int, float, str, bool, list, dict)):
                updated_row[key] = str(val)
                
        return jsonify({"success": True, "booking": updated_row})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- Menu Endpoints ---
@app.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, category, name, description, price FROM menu_items ORDER BY id")
        menu_items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(menu_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/menu', methods=['POST'])
def add_menu_item():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    category = data.get('category')
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    if not category or not name or not price:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO menu_items (category, name, description, price)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """, (category, name, description, price))
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "item": item})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/menu/<int:id>', methods=['PUT'])
def update_menu_item(id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    category = data.get('category')
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    if not category or not name or not price:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            UPDATE menu_items
            SET category = %s, name = %s, description = %s, price = %s
            WHERE id = %s
            RETURNING *
        """, (category, name, description, price, id))
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not item:
            return jsonify({"success": False, "message": "Item not found"}), 404
        return jsonify({"success": True, "item": item})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/menu/<int:id>', methods=['DELETE'])
def delete_menu_item(id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM menu_items WHERE id = %s RETURNING id", (id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not deleted:
            return jsonify({"success": False, "message": "Item not found"}), 404
        return jsonify({"success": True, "message": "Menu item deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- Gallery Endpoints ---
@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, url, caption, category FROM gallery_items ORDER BY id")
        gallery_items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(gallery_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/gallery', methods=['POST'])
def add_gallery_item():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    url = data.get('url')
    caption = data.get('caption')
    category = data.get('category')
    if not url or not caption or not category:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO gallery_items (url, caption, category)
            VALUES (%s, %s, %s)
            RETURNING *
        """, (url, caption, category))
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True, "item": item})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/gallery/<int:id>', methods=['DELETE'])
def delete_gallery_item(id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM gallery_items WHERE id = %s RETURNING id", (id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not deleted:
            return jsonify({"success": False, "message": "Gallery item not found"}), 404
        return jsonify({"success": True, "message": "Gallery item deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

