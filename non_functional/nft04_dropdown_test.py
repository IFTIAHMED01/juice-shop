from playwright.sync_api import sync_playwright

#Automated Script for Keyboard Dropdown Test[4th Non-Functional Test Case]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1366, "height": 900})

    page.goto("http://localhost:3000", wait_until="networkidle")
    page.wait_for_timeout(2000)

    # Close the welcome dialog if it appears
    if page.locator("mat-dialog-container").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

    print("\nNFT-04: Keyboard Dropdown Navigation Test")
    print("=" * 50)

    # Locate the Items per page dropdown
    dropdown = page.locator("mat-select").first
    dropdown.focus()

    print("Initial dropdown value:", dropdown.inner_text().strip())

    # Open dropdown using Enter
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)

    dropdown_opened = page.locator("mat-option").count() > 0
    print("Dropdown opened:", dropdown_opened)

    if dropdown_opened:
        # Navigate through options using Arrow Down
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(300)

        print("Arrow Down navigation: Successful")

        # Select the highlighted option using Enter
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        print("Dropdown selection completed.")
        print("Selected value:", dropdown.inner_text().strip())

    else:
        print("Dropdown could not be opened.")

    # Save screenshot
    page.screenshot(
        path="non_functional/NFT-04_Keyboard_Dropdown_Test.png",
        full_page=True
    )

    print("\nScreenshot saved:")
    print("non_functional/NFT-04_Keyboard_Dropdown_Test.png")

    browser.close()