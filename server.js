const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json({limit: '10mb'}));
app.use(express.static('.'));
app.use('/uploads', express.static('uploads'));

const contactsFile = './contacts.json';
const uploadsDir = './uploads';

if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Get contacts
app.get('/api/contacts', (req, res) => {
    const contacts = JSON.parse(fs.readFileSync(contactsFile, 'utf8'));
    res.json(contacts);
});

// Add contact
app.post('/api/contacts', (req, res) => {
    const contact = req.body;
    
    if (contact.photo) {
        const base64Data = contact.photo.replace(/^data:image\/\w+;base64,/, '');
        const filename = `${Date.now()}_${contact.name.replace(/\s+/g, '_')}.jpg`;
        const filepath = path.join(uploadsDir, filename);
        
        fs.writeFileSync(filepath, base64Data, 'base64');
        contact.photo = `/uploads/${filename}`;
    }
    
    const contacts = JSON.parse(fs.readFileSync(contactsFile, 'utf8'));
    contacts.push(contact);
    fs.writeFileSync(contactsFile, JSON.stringify(contacts, null, 2));
    res.json({success: true});
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
    console.log('Images stored in: ./uploads/');
});