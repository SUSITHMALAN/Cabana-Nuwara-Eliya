import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for the frontend to communicate with the backend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("Warning: Supabase credentials not found. Ensure SUPABASE_URL and SUPABASE_KEY are set.")

@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok", "message": "Backend API is running."})

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    try:
        # Fetch all rooms, ordering by id
        response = supabase.table("rooms").select("*").order("id").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    try:
        response = supabase.table("testimonials").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/amenities', methods=['GET'])
def get_amenities():
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    try:
        response = supabase.table("amenities").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/book', methods=['POST'])
def book():
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    
    data = request.json
    required_fields = ['cabana_id', 'checkin', 'checkout', 'guests', 'fname', 'lname', 'email', 'phone']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    try:
        # Insert booking into the database
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
        
        response = supabase.table("bookings").insert(booking_data).execute()
        
        # WhatsApp logic
        admin_number = "94771758395"
        cabana_name = "Main Cabana" if booking_data['cabana_id'] == 1 else "Little Eury Nature Cabana"
        msg = f"Hello Admin! I would like to book {cabana_name} for {booking_data['guests']} guests from {booking_data['checkin']} to {booking_data['checkout']} ({booking_data['days_spent']} nights). My name is {booking_data['fname']} {booking_data['lname']}."
        import urllib.parse
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
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    
    data = request.json
    required_fields = ['fname', 'lname', 'email', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    try:
        contact_data = {
            "fname": data.get('fname'),
            "lname": data.get('lname'),
            "email": data.get('email'),
            "phone": data.get('phone'),
            "subject": data.get('subject'),
            "message": data.get('message')
        }
        
        response = supabase.table("contacts").insert(contact_data).execute()
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
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    try:
        response = supabase.table("bookings").select("*, rooms(name)").order("created_at", desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/bookings/<int:id>/status', methods=['PUT'])
def update_booking_status(id):
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    
    data = request.json
    status = data.get('status')
    if not status:
        return jsonify({"error": "Status is required"}), 400

    try:
        response = supabase.table("bookings").update({"status": status}).eq("id", id).execute()
        if not response.data:
            return jsonify({"error": "Booking not found"}), 404
        
        booking = response.data[0]
        
        # If confirmed, generate whatsapp URL for guest
        wa_url = None
        if status == 'confirmed':
            # Format phone number for whatsapp (remove leading 0 and add 94, assuming SL number)
            phone = booking.get('phone', '')
            formatted_phone = "94" + phone[1:] if phone.startswith('0') else phone
            msg = f"Hello {booking.get('fname')}, your booking for Cabana from {booking.get('checkin')} to {booking.get('checkout')} is CONFIRMED. Thank you for choosing Eury Nature Cabana!"
            import urllib.parse
            wa_url = f"https://wa.me/{formatted_phone}?text={urllib.parse.quote(msg)}"

        return jsonify({"success": True, "booking": booking, "whatsapp_url": wa_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/contacts', methods=['GET'])
def get_contacts():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    if not supabase:
        return jsonify({"error": "Database connection not configured"}), 500
    try:
        response = supabase.table("contacts").select("*").order("created_at", desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 by default
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
