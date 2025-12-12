from app.config.firebase_init import db

def save_event(event):
    db.collection("competitions").add(event)
