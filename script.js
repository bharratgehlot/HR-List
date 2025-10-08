let contacts = [];

// Load contacts on page load
document.addEventListener('DOMContentLoaded', function() {
    loadContacts();
});

// Form submission handler
document.getElementById('hrForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const photoFile = document.getElementById('photo').files[0];
    let photoData = null;
    
    if (photoFile) {
        photoData = await convertToBase64(photoFile);
    }
    
    const contact = {
        name: document.getElementById('name').value,
        number: document.getElementById('number').value,
        company: document.getElementById('company').value,
        location: document.getElementById('location').value,
        email: document.getElementById('email').value,
        status: document.getElementById('status').value,
        photo: photoData
    };
    
    await saveContact(contact);
    await loadContacts();
    
    // Reset form
    document.getElementById('hrForm').reset();
});

// Convert file to base64
function convertToBase64(file) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.readAsDataURL(file);
    });
}

// Save contact to JSON file via server
async function saveContact(contact) {
    await fetch('/api/contacts', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(contact)
    });
}

// Load contacts from JSON file via server
async function loadContacts() {
    const response = await fetch('/api/contacts');
    contacts = await response.json();
    displayContacts();
}

// Display contacts in table
function displayContacts() {
    const tbody = document.getElementById('contactTableBody');
    tbody.innerHTML = '';
    
    contacts.forEach(contact => {
        const row = tbody.insertRow();
        const photoCell = contact.photo 
            ? `<img src="${contact.photo}" class="profile-pic" alt="Profile">` 
            : `<img src="placeholder.svg" class="profile-pic" alt="No Photo">`;
        
        row.innerHTML = `
            <td>${photoCell}</td>
            <td>${contact.name}</td>
            <td>${contact.number}</td>
            <td>${contact.company}</td>
            <td>${contact.location}</td>
            <td>${contact.email}</td>
            <td>${contact.status}</td>
        `;
    });
}