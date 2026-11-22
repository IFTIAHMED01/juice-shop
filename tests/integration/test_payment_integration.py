
import requests
import uuid

BASE_URL = "http://localhost:3000"


# IT-01: Payment Card Creation and Retrieval [1st Test Case]
def test_create_and_retrieve_payment_card():

    # Step 1: Register a new user
    email = f"paymentuser-{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPassword123!"

    registration_payload = {
        "email": email,
        "password": password,
        "passwordRepeat": password,
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

    # Verify successful registration
    assert registration_response.status_code == 201
    assert registration_response.json()["status"] == "success"

    # Step 2: Log in with the newly registered user
    login_response = requests.post(
        f"{BASE_URL}/rest/user/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()
    token = login_data["authentication"]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Step 3: Create a new payment card
    card_payload = {
        "fullName": "Integration Test User",
        "cardNum": 4111111111111111,
        "expMonth": 12,
        "expYear": 2099
    }

    card_response = requests.post(
        f"{BASE_URL}/api/Cards",
        json=card_payload,
        headers=headers
    )

    # Verify successful card creation
    assert card_response.status_code == 201
    assert card_response.json()["status"] == "success"

    card_data = card_response.json()
    card_id = card_data["data"]["id"]

    # Step 4: Retrieve the saved payment card
    retrieve_response = requests.get(
        f"{BASE_URL}/api/Cards/{card_id}",
        headers=headers
    )

    # Verify successful retrieval
    assert retrieve_response.status_code == 200

    retrieved_card = retrieve_response.json()["data"]

    # Verify that the card information is correct
    assert retrieved_card["id"] == card_id
    assert retrieved_card["fullName"] == "Integration Test User"

    # Verify that the card number is masked
    assert retrieved_card["cardNum"] == "************1111"