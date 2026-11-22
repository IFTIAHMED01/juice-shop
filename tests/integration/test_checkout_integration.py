
import requests
import uuid

BASE_URL = "http://localhost:3000"

#Testing checkout integration[2nd test case of Integration Testing]
def test_checkout_and_verify_order_history():
    # Step 1: Register a new user
    unique_email = f"it02_{uuid.uuid4().hex[:8]}@example.com"

    register_payload = {
        "email": unique_email,
        "password": "TestPassword123!",
        "passwordRepeat": "TestPassword123!",
        "securityQuestion": {
            "id": 1,
            "question": "Your eldest siblings middle name?"
        },
        "securityAnswer": "testanswer"
    }

    register_response = requests.post(
        f"{BASE_URL}/api/Users",
        json=register_payload
    )

    assert register_response.status_code == 201
    assert register_response.json()["status"] == "success"

    # Step 2: Log in as the newly registered user
    login_response = requests.post(
        f"{BASE_URL}/rest/user/login",
        json={
            "email": unique_email,
            "password": "TestPassword123!"
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

    # Step 3: Add Apple Juice to the user's basket
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

    # Step 4: Verify that the basket contains Apple Juice
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

    # Step 5: Complete checkout
    checkout_response = requests.post(
        f"{BASE_URL}/rest/basket/{basket_id}/checkout",
        headers=headers
    )

    assert checkout_response.status_code == 200

    order_confirmation = checkout_response.json()["orderConfirmation"]
    assert order_confirmation is not None

    # Step 6: Retrieve the user's order history
    history_response = requests.get(
        f"{BASE_URL}/rest/order-history",
        headers=headers
    )

    assert history_response.status_code == 200
    assert history_response.json()["status"] == "success"

    orders = history_response.json()["data"]

    # Step 7: Verify that the newly created order appears in history
    created_order = next(
        (order for order in orders
         if order["orderId"] == order_confirmation),
        None
    )

    assert created_order is not None
    assert len(created_order["products"]) > 0