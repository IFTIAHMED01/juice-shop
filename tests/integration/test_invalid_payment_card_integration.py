
import requests
import uuid

BASE_URL = "http://localhost:3000"


#Testing invalid payment card integration[3rd Test Case of Integration Testing]
def test_reject_invalid_payment_card():
    # Step 1: Register a new user
    unique_email = f"it03_{uuid.uuid4().hex[:8]}@example.com"

    registration_payload = {
        "email": unique_email,
        "password": "TestPassword123!",
        "passwordRepeat": "TestPassword123!",
        "securityQuestion": {
            "id": 1,
            "question": "Your eldest siblings middle name?"
        },
        "securityAnswer": "testanswer"
    }

    registration_response = requests.post(
        f"{BASE_URL}/api/Users",
        json=registration_payload
    )

    assert registration_response.status_code == 201
    assert registration_response.json()["status"] == "success"

    # Step 2: Log in as the newly registered user
    login_response = requests.post(
        f"{BASE_URL}/rest/user/login",
        json={
            "email": unique_email,
            "password": "TestPassword123!"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["authentication"]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Step 3: Submit a payment card with an invalid card number
    invalid_card_payload = {
        "fullName": "Integration Test User",
        "cardNum": 12345678876543210,
        "expMonth": 1,
        "expYear": 2085
    }

    card_response = requests.post(
        f"{BASE_URL}/api/Cards",
        json=invalid_card_payload,
        headers=headers
    )

    # Step 4: Verify that the application rejects the invalid card
    assert card_response.status_code == 400