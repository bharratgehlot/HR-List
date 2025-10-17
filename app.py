from flask import Flask, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
load_dotenv()
import base64
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
UPLOADS_DIR = 'uploads'

if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def get_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        contacts = cursor.fetchall()
        conn.close()
        return jsonify([dict(contact) for contact in contacts])
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return jsonify([])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    try:
        contact = request.json
        
        if contact.get('photo'):
            photo_data = contact['photo'].split(',')[1]
            filename = f"{int(datetime.now().timestamp())}_{contact['name'].replace(' ', '_')}.jpg"
            filepath = os.path.join(UPLOADS_DIR, filename)
            
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(photo_data))
            
            contact['photo'] = f'/uploads/{filename}'
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacts (photo, name, company, location, position, number, email, status, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            contact.get('photo'),
            contact['name'],
            contact['company'],
            contact['location'],
            contact.get('position'),
            contact['number'],
            contact['email'],
            contact['status'],
            contact.get('url')
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding contact: {e}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
