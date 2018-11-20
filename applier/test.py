import requests

test_json = {
        'firstName': 'Alex',
        'lastName': 'Sieusahai',
        'email': 'alexsieu14@gmail.com',
        'password': 'password123'
        }

#something = requests.post('http://localhost:5000/register', json = test_json)
something = requests.post('http://localhost:5000/setinformation', json = test_json)

print(something.json())
