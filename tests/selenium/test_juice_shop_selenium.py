import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:3000"

#Verify homepage loads [1st Test Case]
def test_homepage_loads_successfully(driver):
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    # Close the welcome banner if it appears
    try:
        close_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Close Welcome Banner"]')
            )
        )
        close_button.click()
    except Exception:
        pass

    # Verify the homepage title
    assert driver.title == "OWASP Juice Shop"

    # Verify the homepage navigation is visible
    home_button = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="Back to homepage"]')
        )
    )

    assert home_button.is_displayed()


#Search for a Product[2nd Test Case]
def test_search_product(driver):
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    # Close welcome banner if it appears
    try:
        close_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Close Welcome Banner"]')
            )
        )
        close_button.click()
    except Exception:
        pass

    # Open search
    search_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="Open search"]')
        )
    )
    search_button.click()

    # Enter product name
    search_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[autocapitalize="none"]')
        )
    )
    search_input.send_keys("Apple Juice")

    # Verify matching product appears
    product = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apple juice')]")
        )
    )

    assert "apple juice" in product.text.lower()


#Login with Invalid Credentials[3rd Test Case]
def test_login_with_invalid_credentials(driver):
    driver.get(BASE_URL + "/#/login")

    wait = WebDriverWait(driver, 15)

    # Close the welcome dialog if it appears
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Close Welcome Banner"]')
            )
        )
        close_button.click()
    except Exception:
        pass

    # Dismiss the cookie consent popup if it appears
    try:
        cookie_popup = driver.find_element(
            By.CSS_SELECTOR, ".cc-window"
        )

        if cookie_popup.is_displayed():
            driver.execute_script(
                """
                document.querySelector(
                    'a[aria-label="dismiss cookie message"]'
                ).click();
                """
            )

            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".cc-window")
                )
            )
    except Exception:
        pass

    # Enter invalid email and password
    email_input = wait.until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys("invalid_user@example.com")
    password_input.send_keys("WrongPassword123")

    # Wait for any existing snackbar notification to disappear
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")
        )
    )

    # Click the login button
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "loginButton"))
    )
    login_button.click()

    # Verify that the user remains on the login page
    wait.until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    assert "#/login" in driver.current_url


#User Registration and Login Workflow[4th Test Case]
def test_registration_and_login_workflow(driver):
    driver.get(BASE_URL + "/#/register")

    wait = WebDriverWait(driver, 20)

    # Close the welcome dialog if it appears
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Close Welcome Banner"]')
            )
        )
        close_button.click()
    except Exception:
        pass

    # Dismiss the cookie consent popup if it appears
    try:
        cookie_popup = driver.find_element(
            By.CSS_SELECTOR, ".cc-window"
        )

        if cookie_popup.is_displayed():
            driver.execute_script(
                """
                document.querySelector(
                    'a[aria-label="dismiss cookie message"]'
                ).click();
                """
            )
    except Exception:
        pass

    
    # Generate a unique email for registration
    email = "selenium_" + uuid.uuid4().hex[:10] + "@example.com"
    password = "TestPass123!"

    # Fill in the registration form
    email_input = wait.until(
        EC.visibility_of_element_located((By.ID, "emailControl"))
    )
    email_input.send_keys(email)

    driver.find_element(
        By.ID, "passwordControl"
    ).send_keys(password)

    driver.find_element(
        By.ID, "repeatPasswordControl"
    ).send_keys(password)

    # Wait for the snackbar notification to disappear
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")
        )
    )

    # Select the security question
    security_question = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "securityQuestionControl")
        )
    )
    security_question.click()

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//mat-option[.//span[contains(text(), 'Your favorite book?')]]"
            )
        )
    ).click()

    # Enter the security answer
    answer_input = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "securityAnswerControl")
        )
    )
    answer_input.send_keys("Harry Potter")

    # Submit the registration form
    register_button = wait.until(
        EC.element_to_be_clickable((By.ID, "registerButton"))
    )
    register_button.click()

    # Wait for the login page to appear
    email_login = wait.until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    # Enter the newly registered account details
    email_login.send_keys(email)

    driver.find_element(
        By.ID, "password"
    ).send_keys(password)

    # Wait for the snackbar notification to disappear
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")
        )
    )

    # Click the login button
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "loginButton"))
    )
    login_button.click()

    # Verify successful login
    wait.until(
        lambda d: "#/login" not in d.current_url
    )

    assert "#/login" not in driver.current_url


#Add Product to Basket and Verify[5th Test Case]
def test_add_product_to_basket(driver):
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 20)

    # Close the welcome dialog if it appears
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Close Welcome Banner"]')
            )
        )
        close_button.click()
    except Exception:
        pass

    # Dismiss the cookie consent popup if it appears
    try:
        cookie_popup = driver.find_element(
            By.CSS_SELECTOR, ".cc-window"
        )

        if cookie_popup.is_displayed():
            driver.execute_script(
                """
                document.querySelector(
                    'a[aria-label="dismiss cookie message"]'
                ).click();
                """
            )
    except Exception:
        pass

    # Open the search field
    search_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="Open search"]')
        )
    )
    search_button.click()

    # Search for Apple Juice
    search_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[autocapitalize="none"]')
        )
    )
    search_input.send_keys("Apple Juice")

    # Locate the Apple Juice product card
    product_card = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//mat-card[.//*[contains(translate(., "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), 'apple juice')]]"
            )
        )
    )

    # Wait for the snackbar notification to disappear
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".mat-mdc-snack-bar-label")
        )
    )

    # Locate and click the Add to Basket button
    add_button = product_card.find_element(
        By.CSS_SELECTOR,
        'button[aria-label="Add to Basket"]'
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        add_button
    )

    wait.until(
        lambda d: add_button.is_displayed() and add_button.is_enabled()
    )

    add_button.click()

    # Open the shopping cart
    cart_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="Show the shopping cart"]')
        )
    )
    cart_button.click()

    # Verify Apple Juice appears in the basket
    basket_product = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(translate(., "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), 'apple juice')]"
            )
        )
    )

    assert "apple juice" in basket_product.text.lower()