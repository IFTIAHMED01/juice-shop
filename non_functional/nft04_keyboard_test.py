from playwright.sync_api import sync_playwright
import json

results = []

#Automated Script for Keyboard Navigation Test[4th Non-Functional Test Case]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1366, "height": 900})

    page.goto("http://localhost:3000", wait_until="networkidle")
    page.wait_for_timeout(3000)

    # Close the welcome dialog if it appears
    if page.locator("mat-dialog-container").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

    print("\nNFT-04: Keyboard Navigation Test")
    print("=" * 50)
    print("Page title:", page.title())

    # Test 1: Sequential keyboard focus
    print("\nTest 1: Sequential Keyboard Focus")

    for i in range(1, 21):
        page.keyboard.press("Tab")
        page.wait_for_timeout(150)

        focused = page.evaluate("""() => {
            const el = document.activeElement;
            const style = window.getComputedStyle(el);

            return {
                tag: el.tagName,
                text: (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 70),
                focusOutline: style.outlineStyle,
                outlineWidth: style.outlineWidth,
                outlineColor: style.outlineColor
            };
        }""")

        print(f"Tab {i}: {focused}")
        results.append({"tab": i, **focused})

    # Test 2: Check interactive elements and accessible names
    print("\nTest 2: Interactive Elements and Accessible Names")

    elements = page.locator(
        "button, a, input, select, [role='button'], [role='combobox']"
    ).evaluate_all("""els =>
        els.slice(0, 40).map(el => ({
            tag: el.tagName,
            text: (el.innerText || '').trim().slice(0, 60),
            ariaLabel: el.getAttribute('aria-label'),
            title: el.getAttribute('title'),
            accessibleNamePresent: !!(
                (el.innerText || '').trim() ||
                el.getAttribute('aria-label') ||
                el.getAttribute('title') ||
                el.getAttribute('placeholder')
            )
        }))
    """)

    for element in elements:
        print(element)

    # Save test results
    with open("non_functional/nft04_keyboard_results.json", "w") as f:
        json.dump({
            "page_title": page.title(),
            "keyboard_focus_results": results,
            "interactive_elements": elements
        }, f, indent=4)

    # Save screenshot
    page.screenshot(
        path="non_functional/NFT-04_Keyboard_Navigation.png",
        full_page=True
    )

    print("\nResults saved successfully:")
    print("non_functional/nft04_keyboard_results.json")
    print("non_functional/NFT-04_Keyboard_Navigation.png")

    browser.close()