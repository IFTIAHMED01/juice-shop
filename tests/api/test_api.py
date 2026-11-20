
import requests


BASE_URL = "http://localhost:3000"


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