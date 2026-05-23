# 🏡 Cabana Nuwara Eliya — Hotel Website

A full-stack hotel website for **Cabana Nuwara Eliya**, built with:
- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

Inspired by Hotel Cabana Clearwater Beach — featuring a hero image slider,
animated scroll reveals, testimonials carousel, booking modal, gallery
with filter, and a full multi-page layout.

---

## 📁 Project Structure

```
cabana_nuwaraeliya/
├── app.py                  # Flask application (routes + data)
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet (all pages)
│   └── js/
│       └── main.js         # All animations & interactions
└── templates/
    ├── base.html           # Base layout (navbar + footer)
    ├── index.html          # Homepage (hero, rooms, gallery, etc.)
    ├── accommodations.html # Rooms & Suites page
    ├── amenities.html      # Amenities page
    ├── gallery.html        # Gallery with filter
    ├── dining.html         # Dining page
    ├── discover.html       # Discover Nuwara Eliya page
    └── contact.html        # Contact form page
```

---

## 🚀 Setup & Run

### 1. Install Python 3.8+
Make sure Python is installed on your machine.

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python app.py
```

### 5. Open your browser
```
http://localhost:5000
```

---

## 🌐 Pages

| URL              | Description                        |
|------------------|------------------------------------|
| `/`              | Homepage with hero slider          |
| `/accommodations`| Rooms & Suites                     |
| `/amenities`     | Hotel amenities                    |
| `/gallery`       | Photo gallery with filter tabs     |
| `/dining`        | Restaurant & Bar                   |
| `/discover`      | Discover Nuwara Eliya              |
| `/contact`       | Contact form                       |
| `/api/book`      | Booking API (POST, JSON)           |

---

## ✨ Features

- 🎠 **Auto-advancing Hero Slider** with 4 slides, swipe support, arrows & dots
- 📅 **Booking Modal** with check-in/check-out date picker
- 📊 **Animated Counters** (guests, rooms, ratings)
- 🎭 **Scroll Reveal Animations** on all sections (fade up, left, right)
- 🖼️ **Gallery** with category filter (All / Rooms / Dining / Pool / Gardens / Views)
- 💬 **Testimonials Carousel** with auto-advance
- 📱 **Fully Responsive** — mobile hamburger menu, stacked layouts
- 🍪 **Cookie Notice** (GDPR-friendly, localStorage)
- 📈 **Scroll Progress Bar** at the top
- 🔝 **Back-to-Top Button**
- 🌙 **Page Loader** animation on first load
- 🖼️ **Lightbox** for gallery images

---

## 🛠️ Customisation

### Replace demo gradient backgrounds with real images
In `style.css`, find `.slide-1`, `.slide-2`, etc. and replace with:
```css
.slide-1 {
    background-image: url('/static/images/hero1.jpg');
}
```

Do the same for `.r1`, `.r2` (room cards) and `.g1`, `.g2` (gallery items).

### Update hotel info
Edit `app.py` — the `ROOMS`, `TESTIMONIALS`, and `AMENITIES` lists at the top.

### Change colours
Edit the CSS variables in `style.css`:
```css
:root {
    --primary: #2c5f2e;   /* main green */
    --gold: #b89650;       /* gold accent */
    --cream: #faf6f0;      /* background */
}
```

---

## 📧 Email Integration (Production)
In `app.py`, the `/contact` route currently just returns JSON.
To send real emails, install Flask-Mail:
```bash
pip install Flask-Mail
```

---

*Built with ❤️ for Cabana Nuwara Eliya, Sri Lanka*
