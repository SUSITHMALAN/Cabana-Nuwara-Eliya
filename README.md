# 🏡 Eury Nature Cabana Nuwara Eliya — Hotel Website

Live URL: [https://www.eurynature.com.lk](https://www.eurynature.com.lk)

A full-stack, responsive booking and content management website for **Eury Nature Cabana Nuwara Eliya**, Sri Lanka.

---

## 📁 Project Structure

```
cabana_nuwaraeliya/
├── backend/                # Flask application (API server)
│   ├── app.py              # Main backend logic & API routes
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Render deployment blueprint
│   └── .env                # Backend environment variables
├── frontend/               # Static frontend website files
│   ├── index.html          # Homepage
│   ├── accommodations.html # Cabanas details & booking page
│   ├── amenities.html      # Amenities listing
│   ├── gallery.html        # Dynamic media gallery
│   ├── dining.html         # Dynamic restaurant menu
│   ├── discover.html       # Nuwara Eliya attractions
│   ├── contact.html        # Contact form
│   ├── admin.html          # Admin panel
│   ├── book.html           # Booking details form
│   ├── static/             # Frontend assets (CSS, JS, images)
│   └── vercel.json         # Vercel deployment configuration
└── database/               # Database schemas & migrations
    └── schema.sql          # PostgreSQL database schema
```

---

## 🚀 Setup & Run Locally

### 1. Backend API (Flask)
The backend requires Python 3.8+ and a PostgreSQL database.

```bash
# Navigate to backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file (use .env.example as a template)
# Run the flask server
python app.py
```
By default, the backend will run at `http://localhost:5000`.

### 2. Frontend
You can serve the `frontend/` folder using any static file server (e.g., Live Server in VS Code, Python's http.server, or Node's serve).

```bash
# Serve frontend using Python
cd frontend
python -m http.server 8000
```
Open `http://localhost:8000` in your web browser.

---

## 🌐 API Endpoints

| URL | Method | Description |
|---|---|---|
| `/api/health` | GET | Health check status |
| `/api/rooms` | GET | List available cabanas |
| `/api/testimonials` | GET | Get client testimonials |
| `/api/amenities` | GET | List hotel amenities |
| `/api/book` | POST | Submit booking reservation |
| `/api/bookings` | GET/POST/PUT | Admin view and update bookings |
| `/api/menu` | GET/POST/PUT/DELETE | Admin CRUD for dining menu |
| `/api/gallery` | GET/POST/DELETE | Admin CRUD for gallery media |

---

## ✨ Features

- 🎠 **Auto-advancing Hero Slider** with property photos, swipe support, arrows & dots.
- 📅 **Booking Modal & Calendar** with check-in/check-out date picker.
- 🛡️ **Overlap Prevention**: Restricts room double-booking on overlapping dates.
- 🚫 **Past Date Validation**: Prevents reserving dates in the past.
- 📱 **Direct WhatsApp Redirection**: Automatically opens WhatsApp on guest confirmation, pre-populating reservation details for immediate booking contact.
- 🔐 **Secure Admin Portal** (`admin.html`) with login authentication to manage:
  - **Reservations**: View, confirm, cancel, and WhatsApp guests directly.
  - **Dining Menu**: Dynamically add, edit, or delete items shown on the site.
  - **Gallery**: Real-time gallery content updates (photos/videos).
- 🍪 **Cookie Notice** (GDPR-friendly, localStorage).
- 🔝 **Back-to-Top Button** & **Scroll Progress Indicator**.
- 🎨 **Responsive Design** optimized for all screens (mobiles, tablets, desktops).

---

## 📧 Deployment Details

- **Frontend**: Hosted on Vercel
- **Backend API**: Hosted on Render
- **Database**: PostgreSQL (e.g., Neon or Supabase)

*Built with ❤️ for Eury Nature Cabana, Nuwara Eliya, Sri Lanka*
