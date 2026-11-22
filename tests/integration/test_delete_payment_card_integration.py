import requests
import uuid

BASE_URL = "http://localhost:3000"


#Testing deleting payment card integration[4th Test Case]
def test_delete_payment_card_and_verify_removal():
    # Step 1: Register a new user
    unique_email = f"it04_{uuid.uuid4().hex[:8]}@example.com"

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

    # Step 3: Create a payment card
    card_payload = {
        "fullName": "Integration Test User",
        "cardNum": 1234567812341111,
        "expMonth": 12,
        "expYear": 2085
    }

    create_response = requests.post(
        f"{BASE_URL}/api/Cards",
        json=card_payload,
        headers=headers
    )

    assert create_response.status_code == 201
    assert create_response.json()["status"] == "success"

    card_id = create_response.json()["data"]["id"]

    # Step 4: Delete the newly created payment card
    delete_response = requests.delete(
        f"{BASE_URL}/api/Cards/{card_id}",
        headers=headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "success"
    assert delete_response.json()["data"] == "Card deleted successfully."

    # Step 5: Attempt to retrieve the deleted payment card
    retrieve_response = requests.get(
        f"{BASE_URL}/api/Cards/{card_id}",
        headers=headers
    )

    # Step 6: Verify that the deleted card is no longer available
    assert retrieve_response.status_code == 400
    assert retrieve_response.json()["status"] == "error"
    assert retrieve_response.json()["data"] == "Malicious activity detected"