import csv
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "http://localhost:3000"
OUTPUT_DIR = Path("non_functional")
RESULTS = []

#Server Response Test[5th Test Case]
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/home/codespace/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome",
        args=["--no-sandbox"]
    )

    context = browser.new_context()
    page = context.new_page()

    # Disable browser cache for consistent measurements.
    cdp = context.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})

    print("NFT-05: Server Response Time Test")
    print("=" * 45)

    for attempt in range(1, 6):
        response = page.goto(URL, wait_until="load", timeout=60000)

        timing = page.evaluate("""
            () => {
                const entry = performance.getEntriesByType('navigation')[0];
                return {
                    requestStart: entry.requestStart,
                    responseStart: entry.responseStart
                };
            }
        """)

        ttfb = round(
            timing["responseStart"] - timing["requestStart"], 2
        )

        status = response.status if response else None

        RESULTS.append({
            "measurement": attempt,
            "http_status": status,
            "ttfb_ms": ttfb
        })

        print(
            f"Measurement {attempt}: "
            f"HTTP {status}, TTFB = {ttfb} ms"
        )

    # Capture evidence of the application after testing.
    page.screenshot(
        path=str(OUTPUT_DIR / "NFT-05_Server_Response_Results.png"),
        full_page=True
    )

    browser.close()

successful = [r for r in RESULTS if r["http_status"] == 200]

ttfb_values = [r["ttfb_ms"] for r in RESULTS]

summary = {
    "test_id": "NFT-05",
    "test_name": "Verify Server Response Time Using Browser Developer Tools",
    "url": URL,
    "test_date_utc": datetime.now(timezone.utc).isoformat(),
    "total_measurements": len(RESULTS),
    "successful_responses": len(successful),
    "average_ttfb_ms": round(statistics.mean(ttfb_values), 2),
    "minimum_ttfb_ms": round(min(ttfb_values), 2),
    "maximum_ttfb_ms": round(max(ttfb_values), 2),
    "measurements": RESULTS
}

with open(OUTPUT_DIR / "nft05_response_results.json", "w") as f:
    json.dump(summary, f, indent=4)

with open(OUTPUT_DIR / "nft05_response_summary.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=["measurement", "http_status", "ttfb_ms"]
    )
    writer.writeheader()
    writer.writerows(RESULTS)

print("\n" + "=" * 45)
print("TEST SUMMARY")
print(f"Successful responses: {len(successful)}/5")
print(f"Average TTFB: {summary['average_ttfb_ms']} ms")
print(f"Minimum TTFB: {summary['minimum_ttfb_ms']} ms")
print(f"Maximum TTFB: {summary['maximum_ttfb_ms']} ms")
print("\nResults and screenshot saved in non_functional/")
