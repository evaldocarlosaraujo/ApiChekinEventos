from firebase_admin import db
import uuid

def create_event(data):
    ref = db.reference('/events')
    event_id = str(uuid.uuid4())
    ref.child(event_id).set(data)
    return {"id": event_id, "message": "Event created successfully"}

def get_events():
    ref = db.reference('/events')
    return ref.get()

def get_event(event_id):
    ref = db.reference(f'/events/{event_id}')
    return ref.get()

def update_event(event_id, data):
    ref = db.reference(f'/events/{event_id}')
    ref.update(data)
    return {"message": "Event updated successfully"}

def delete_event(event_id):
    ref = db.reference(f'/events/{event_id}')
    ref.delete()
    return {"message": "Event deleted successfully"}
