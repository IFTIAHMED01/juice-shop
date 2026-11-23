from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:3000"

#Verify Product Details[Test Case-01]
def test_product_details(page: Page):
    page.goto(BASE_URL)

    # Dismiss the welcome dialog
    page.get_by_role(
        "button", name="Close Welcome Banner"
    ).click()

    # Wait until the welcome dialog disappears
    page.locator(
        'button[aria-label="Close Welcome Banner"]'
    ).wait_for(state="hidden")

    # Dismiss the cookie popup
    page.locator(
        'a[aria-label="dismiss cookie message"]'
    ).evaluate("(element) => element.click()")

    # Verify the cookie popup disappears
    page.locator(".cc-window").wait_for(
        state="hidden"
    )

    # Open Apple Juice product details
    page.get_by_text(
        "Apple Juice (1000ml)", exact=True
    ).click()

    # Verify the product details heading
    expect(
        page.get_by_role(
            "heading", name="Apple Juice (1000ml)"
        )
    ).to_be_visible()


#Verify Shopping Basket Opens(2nd Test Case)
def test_shopping_basket_opens(page: Page):
    page.goto(BASE_URL)

    # Dismiss the welcome dialog
    page.get_by_role(
        "button", name="Close Welcome Banner"
    ).click()

    page.locator(
        'button[aria-label="Close Welcome Banner"]'
    ).wait_for(state="hidden")

    # Dismiss cookie popup
    page.locator(
        'a[aria-label="dismiss cookie message"]'
    ).evaluate("(element) => element.click()")

    page.locator(".cc-window").wait_for(
        state="hidden"
    )

    # Open shopping basket
    page.locator(
        'button[aria-label="Show the shopping cart"]'
    ).click()

    # Verify shopping basket page
    expect(page).to_have_url(
        "http://localhost:3000/#/basket"
    )


#Verify Login Form Validation[3rd Test Case]
def test_login_form_validation(page: Page):
    # Open the login page directly
    page.goto(BASE_URL + "/#/login")

    # Dismiss the welcome dialog if displayed
    page.get_by_role(
        "button", name="Close Welcome Banner"
    ).click()

    page.locator(
        'button[aria-label="Close Welcome Banner"]'
    ).wait_for(state="hidden")

    # Dismiss cookie popup
    page.locator(
        'a[aria-label="dismiss cookie message"]'
    ).evaluate("(element) => element.click()")

    page.locator(".cc-window").wait_for(
        state="hidden"
    )

    # Verify login page opens
    expect(page).to_have_url(
        "http://localhost:3000/#/login"
    )

    # Verify login form fields are visible
    expect(page.locator("#email")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()

    # Verify login button is disabled with empty fields
    expect(
        page.locator("#loginButton")
    ).to_be_disabled()


#Verify Navigation Menu[4th Test Case]
def test_navigation_menu(page: Page):
    page.goto(BASE_URL)

    # Dismiss the welcome dialog
    page.get_by_role(
        "button", name="Close Welcome Banner"
    ).click()

    page.locator(
        'button[aria-label="Close Welcome Banner"]'
    ).wait_for(state="hidden")

    # Dismiss cookie popup
    page.locator(
        'a[aria-label="dismiss cookie message"]'
    ).evaluate("(element) => element.click()")

    page.locator(".cc-window").wait_for(
        state="hidden"
    )

    # Open side navigation
    page.locator(
        'button[aria-label="Open Sidenav"]'
    ).click()

    # Verify navigation menu links
    expect(
        page.locator('a[href="#/contact"]')
    ).to_be_visible()

    expect(
        page.locator('a[href="#/about"]')
    ).to_be_visible()

    expect(
        page.locator('a[href="#/chatbot"]')
    ).to_be_visible()

    expect(
        page.locator('a[href="#/photo-wall"]')
    ).to_be_visible()


#Verify Product Search with No Matching Results[5th Test Case]
def test_product_search_no_matching_results(page: Page):
    page.goto(BASE_URL)

    # Dismiss the welcome dialog
    page.get_by_role(
        "button", name="Close Welcome Banner"
    ).click()

    page.locator(
        'button[aria-label="Close Welcome Banner"]'
    ).wait_for(state="hidden")

    # Dismiss cookie popup
    page.locator(
        'a[aria-label="dismiss cookie message"]'
    ).evaluate("(element) => element.click()")

    page.locator(".cc-window").wait_for(
        state="hidden"
    )

    # Open product search
    page.locator(
        'button[aria-label="Open search"]'
    ).click()

    # Search for a nonexistent product
    search_box = page.locator(
        'input[autocapitalize="none"]'
    )

    search_box.fill("NoSuchProductXYZ")

    # Verify that no matching product is displayed
    expect(
        page.get_by_text(
            "NoSuchProductXYZ", exact=True
        )
    ).to_have_count(0)