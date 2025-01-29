import requests

api_url = "https://api.guerrillamail.com/ajax.php"
params = {
    "f": "send_email",
    "email": "ScallAlert@guerrillamail.com",
    "to": "emiliotonix@gmail.com",
    "subject": "Website Down Alert!",
    "body": "Hello,\n\nThis is an automated alert: Your website is down.\n\nAnonymous Bot"
}

response = requests.get(api_url, params=params)
print(response.json())  # Check response for success/failure
