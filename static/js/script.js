document.addEventListener('DOMContentLoaded', function() {
    const elems = document.querySelectorAll('.modal');
    M.Modal.init(elems);
});

document.getElementById('admin-login').addEventListener('click', () => {
    const loginModal = M.Modal.getInstance(document.getElementById('login-modal'));
    loginModal.open();
});

document.getElementById('login-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const username = document.getElementById('admin-username').value;
    const password = document.getElementById('admin-password').value;
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            M.toast({html: 'Invalid username or password'});
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
