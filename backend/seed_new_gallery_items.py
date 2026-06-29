import os
import psycopg2
from dotenv import load_dotenv

# Load env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DIRECT_URL = os.getenv("DIRECT_URL")

# Images mapping
images = [
    {
        "url": "static/images/cabana_picnic_table.jpg",
        "caption": "Cozy A-frame picnic seating area",
        "category": "cabanas"
    },
    {
        "url": "static/images/fields_and_misty_mountains.jpg",
        "caption": "Panoramic view of agricultural terraced fields and mountains",
        "category": "views"
    },
    {
        "url": "static/images/eury_nature_cabana_signboard.jpg",
        "caption": "Eury Nature Cabana welcome signboard",
        "category": "views"
    },
    {
        "url": "static/images/barbecue_chicken_grill.jpg",
        "caption": "Sizzling evening barbecue grill",
        "category": "dining"
    },
    {
        "url": "static/images/scenic_highland_fields.jpg",
        "caption": "Scenic terraced fields and pine forests",
        "category": "views"
    },
    {
        "url": "static/videos/V1.mp4",
        "caption": "Cabana Video 1",
        "category": "videos"
    },
    {
        "url": "static/videos/V2.mp4",
        "caption": "Cabana Video 2",
        "category": "videos"
    },
    {
        "url": "static/videos/V3.mp4",
        "caption": "Cabana Video 3",
        "category": "videos"
    },
    {
        "url": "static/videos/V4.mp4",
        "caption": "Cabana Video 4",
        "category": "videos"
    }
]

def seed():
    url_to_use = DIRECT_URL or DATABASE_URL
    if not url_to_use:
        print("DATABASE_URL / DIRECT_URL not found in environment!")
        return

    # Strip query parameters for psycopg2 compatibility
    cleaned_url = url_to_use
    if '?' in cleaned_url:
        cleaned_url = cleaned_url.split('?')[0]

    print("Connecting to database...")
    try:
        conn = psycopg2.connect(cleaned_url)
    except Exception as e:
        print(f"Failed to connect. Error: {e}")
        # Try fallback if using Direct URL
        if url_to_use == DIRECT_URL and DATABASE_URL:
            print("Trying fallback DATABASE_URL...")
            cleaned_fallback = DATABASE_URL.split('?')[0] if '?' in DATABASE_URL else DATABASE_URL
            try:
                conn = psycopg2.connect(cleaned_fallback)
            except Exception as e2:
                print(f"Fallback failed. Error: {e2}")
                return
        else:
            return

    cur = conn.cursor()
    print("Database connected successfully!")

    print("Seeding new gallery items...")
    inserted_count = 0
    for img in images:
        # Check if already exists to avoid duplicates
        cur.execute("SELECT COUNT(*) FROM gallery_items WHERE url = %s;", (img["url"],))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute(
                "INSERT INTO gallery_items (url, caption, category) VALUES (%s, %s, %s);",
                (img["url"], img["caption"], img["category"])
            )
            print(f"Inserted: {img['url']}")
            inserted_count += 1
        else:
            print(f"Already exists: {img['url']}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Finished! Successfully inserted {inserted_count} new gallery items.")

if __name__ == "__main__":
    seed()
