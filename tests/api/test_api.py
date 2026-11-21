
import requests


BASE_URL = "http://localhost:3000"


# For API Test CASE 1
def test_get_products():
    # Send a GET request to the Products API
    response = requests.get(f"{BASE_URL}/api/Products")

    # Check that the server responds successfully
    assert response.status_code == 200

    # Check that the response contains valid JSON
    data = response.json()

    # Check the API response status
    assert data["status"] == "success"

    # Check that the product list is not empty
    products = data["data"]
    assert len(products) > 0

    # Check that the first product has the required fields
    first_product = products[0]
    assert "id" in first_product
    assert "name" in first_product
    assert "price" in first_product

# FOR API TEST CASE 2
def test_search_products():
    # Search for products containing the word "apple"
    response = requests.get(
        f"{BASE_URL}/rest/products/search",
        params={"q": "apple"}
    )

    # Check successful HTTP response
    assert response.status_code == 200

    # Check JSON response
    data = response.json()
    assert data["status"] == "success"

    # Check that matching products are returned
    products = data["data"]
    assert len(products) > 0

    # Check required fields and search relevance
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "apple" in product["name"].lower()

# FOR API TEST CASE 3
def test_invalid_login():
    # Send login request with invalid credentials
    payload = {
        "email": "invaliduser@example.com",
        "password": "WrongPassword123"
    }

    response = requests.post(
        f"{BASE_URL}/rest/user/login",
        json=payload
    )

    # Verify that login is rejected
    assert response.status_code == 401

    # Verify the response content type
    assert "text/html" in response.headers["Content-Type"]

    # Verify that no authentication token is returned
    assert "token" not in response.text.lower()

# FOR APT TEST CASE 4
def test_login_missing_password():
    # Send login request without a password
    payload = {
        "email": "invaliduser@example.com"
    }

    response = requests.post(
        f"{BASE_URL}/rest/user/login",
        json=payload
    )

    # Verify that login is rejected
    assert response.status_code == 401

    # Verify the response content type
    assert "text/html" in response.headers["Content-Type"]

    # Verify that no authentication token is returned
    assert "token" not in response.text.lower()

# For API TEST CASE 5
import uuid

def test_registration_with_invalid_email():
    payload = {
        "email": f"invalid-email-{uuid.uuid4().hex[:8]}",
        "password": "TestPassword123",
        "passwordRepeat": "TestPassword123",
        "securityQuestion": {
            "id": 1,
            "question": "Your eldest siblings middle name?"
        },
        "securityAnswer": "testanswer"
    }

    response = requests.post(
        f"{BASE_URL}/api/Users",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "success"
    assert data["data"]["email"] == payload["email"]
    assert "id" in data["data"]

# For API TEST CASE 06

import uuid


def test_registration_with_short_password():
    payload = {
        "email": f"shortpassword-{uuid.uuid4().hex[:8]}@example.com",
        "password": "123",
        "passwordRepeat": "123",
        "securityQuestion": {
            "id": 1,
            "question": "Your eldest siblings middle name?"
        },
        "securityAnswer": "testanswer"
    }

    response = requests.post(
        f"{BASE_URL}/api/Users",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "success"
    assert data["data"]["email"] == payload["email"]
    assert "id" in data["data"]

# For API TEST CASE 07

import uuid


def test_successful_user_registration():
    payload = {
        "email": f"validuser-{uuid.uuid4().hex[:8]}@example.com",
        "password": "StrongPassword123!",
        "passwordRepeat": "StrongPassword123!",
        "securityQuestion": {
            "id": 1,
            "question": "Your eldest siblings middle name?"
        },
        "securityAnswer": "testanswer"
    }

    response = requests.post(
        f"{BASE_URL}/api/Users",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "success"
    assert data["data"]["email"] == payload["email"]
    assert "id" in data["data"]
    assert data["data"]["role"] == "customer"

# FOR API TEST CASE 08


def test_add_product_to_basket():
    # Step 1: Create a fresh user
    email = f"basketuser-{uuid.uuid4().hex[:8]}@example.com"

    registration_payload = {
        "email": email,
        "password": "StrongPassword123!",
        "passwordRepeat": "StrongPassword123!",
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

    # Step 2: Log in with the newly created user
    login_response = requests.post(
        f"{BASE_URL}/rest/user/login",
        json={
            "email": email,
            "password": "StrongPassword123!"
        }
    )

    assert login_response.status_code == 200

    login_data = login_response.json()
    token = login_data["authentication"]["token"]
    basket_id = login_data["authentication"]["bid"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Step 3: Add Apple Juice to the new basket
    basket_payload = {
        "ProductId": 1,
        "BasketId": basket_id,
        "quantity": 1
    }

    add_response = requests.post(
        f"{BASE_URL}/api/BasketItems",
        json=basket_payload,
        headers=headers
    )

    assert add_response.status_code == 200
    assert add_response.json()["status"] == "success"

    # Step 4: Retrieve the basket and verify the product
    basket_response = requests.get(
        f"{BASE_URL}/rest/basket/{basket_id}",
        headers=headers
    )

    assert basket_response.status_code == 200

    products = basket_response.json()["data"]["Products"]

    apple_juice = next(
        (product for product in products if product["id"] == 1),
        None
    )

    assert apple_juice is not None
    assert apple_juice["BasketItem"]["quantity"] == 1