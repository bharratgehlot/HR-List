from flask import Flask, request, jsonify, send_from_directory
import json
import os
import base64
from datetime import datetime

app = Flask(__name__)

CONTACTS_FILE = 'contacts.json'
UPLOADS_DIR = 'uploads'

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_DIR, filename)

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    try:
        with open(CONTACTS_FILE, 'r') as f:
            contacts = json.load(f)
        return jsonify(contacts)
    except FileNotFoundError:
        return jsonify([])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    contact = request.json
    
    if contact.get('photo'):
        # Extract base64 data
        photo_data = contact['photo'].split(',')[1]
        filename = f"{int(datetime.now().timestamp())}_{contact['name'].replace(' ', '_')}.jpg"
        filepath = os.path.join(UPLOADS_DIR, filename)
        
        # Save image file
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(photo_data))
        
        contact['photo'] = f'/uploads/{filename}'
    
    # Load existing contacts
    try:
        with open(CONTACTS_FILE, 'r') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        contacts = []
    
    contacts.append(contact)
    
    # Save updated contacts
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000)) # Production
    app.run(host='0.0.0.0', port=port, debug=False) # Production
  # app.run(debug=True, port=3000) Local