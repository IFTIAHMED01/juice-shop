## README – SOFTWARE QUALITY ASSURANCE PROJECT

OWASP Juice Shop | CSE 534 – Software Quality Assurance

Project overview

This project evaluates selected functional and non-functional aspects of OWASP Juice Shop v20.4.0-SNAPSHOT using unit, API, integration, Selenium, Playwright, and non-functional testing. The application was tested in GitHub Codespaces. Repository: <https://github.com/IFTIAHMED01/juice-shop>.

## Submission contents and related documents

This README provides setup guidance, test commands, test-data notes, and a summary of the recorded outcomes. The detailed objectives, scope, environment, risks, and testing strategies are provided in the separately submitted TestPlan.pdf. The final results and defect analysis are presented in FinalReport.pdf.

## Environment and prerequisites

Application: OWASP Juice Shop v20.4.0-SNAPSHOT. Environment: GitHub Codespaces (Linux). Runtime: Node.js 24.22.2 and npm 11.19.1. Python: 3.14.2. Test tools: pytest 9.2.0, Requests 2.34.2, Vitest 5.1.1, Selenium 4.53.0, Playwright 1.65.2, Chromium 159.0.8154.6, and Lighthouse 13.6.0. Use the supplied requirements.txt for the Python testing dependencies and the application repository instructions for application dependencies.

## Application and test setup

1\. Obtain the OWASP Juice Shop v20.4.0-SNAPSHOT source from the repository listed above and follow its setup instructions. 2. Start the application with npm start. 3. Confirm that it is available at <http://localhost:3000>. 4. Install the Python test dependencies with pip install -r requirements.txt. 5. For Playwright, install Chromium with playwright install chromium. 6. Run the required test suite using the commands below and in the relevant testing sections.

## Test-data preparation

Use test data only. The browser tests use Apple Juice for product search/details and use a generated unique email address for the registration-and-login workflow. The negative tests use invalid login details, empty login fields, a malformed registration email, a weak password, and a product search term with no matching result. Integration tests exercise payment-card, basket, checkout, and order-history operations. When rerunning registration tests, use a fresh unique email address where required; do not place real passwords, tokens, or other credentials in the project files.

## Quick test commands

Unit: npx vitest run tests/unit/utils.unit.test.ts  
API: pytest tests/api/ -v  
Integration: pytest tests/integration/ -v  
Selenium: pytest tests/selenium/test_juice_shop_selenium.py -v  
Playwright: pytest tests/playwright/test_juice_shop_playwright.py -v  
Non-functional keyboard: python non_functional/nft04_keyboard_test.py  
Non-functional dropdown: python non_functional/nft04_dropdown_test.py  
Non-functional response-time: python non_functional/nft05_server_response_test.py

## Consolidated functional results

All 30 functional test cases were executed (100% execution rate). Based on expected application behaviour, 28 passed and 2 failed (93.33% expected-behaviour pass rate). The two failures were API-05 and API-06, which exposed registration-validation defects DEF-01 and DEF-02. The original automated assertions reported all 30 scripts/assertions as passing, but the two API assertions did not enforce the expected validation outcome; therefore, they are counted as functional failures in the final report. The two defects remain open and were not fixed or retested.

## Non-functional results

Five non-functional test IDs were documented across two quality attributes, representing four distinct checks: two performance checks and two accessibility checks. NFT-01 and NFT-02 use the same Lighthouse performance audit and are not separate audit executions. Code coverage was not measured, and the five-request TTFB check was not a load or stress test.

## 1.API Testing

### Overview

API testing was performed on the OWASP Juice Shop application to check whether different API endpoints were working as expected. The tests covered product information, product search, user login, user registration, and basket operations.

### Tools Used

- Python 3.14.2
- pytest 9.2.0
- Requests
- GitHub Codespaces

### Test Cases

A total of 8 API test cases were created and executed. They covered:

1. Retrieving product information.
2. Searching for products.
3. Login with incorrect credentials.
4. Login without providing a password.
5. Registration with an invalid email address.
6. Registration with a weak password.
7. Successful user registration.
8. Adding a product to the basket and retrieving basket information.

### How to Run the Tests

First, install the required libraries:

```
pip install pytest requests
```

Start the OWASP Juice Shop application and make sure it is running at:

<http://localhost:3000>

Then run the API tests using:

```
pytest tests/api/ -v
```

### Test Results

- Total test cases: 8
- Executed: 8
- Passed against expected application behaviour: 6
- Failed against expected application behaviour: 2 (API-05 and API-06)
- Blocked: 0
- Execution rate: 100%
- Expected-behaviour pass rate: 75% (6/8)

### Additional Observation

The original pytest execution reported 8 assertions passing because the API-05 and API-06 assertions did not verify that invalid registration inputs were rejected. When actual application behaviour was compared with the expected validation outcome, API-05 and API-06 failed: the application accepted the malformed email address and weak password and returned HTTP 201. These findings are recorded as DEF-01 (Medium severity/priority, provisional) and DEF-02 (High severity/priority, provisional); both remain open and were not fixed or retested.

## 2. Unit Testing

## Overview

Unit testing was performed on selected utility functions of the OWASP Juice Shop application to check whether they were producing the expected results. Different inputs were used to test the functions.

### Tools Used

- TypeScript
- Vitest 5.1.1
- GitHub Codespaces

### Test Cases

A total of 8 unit test cases were created. They covered:

1. Checking the result of an empty query.
2. Checking whether a valid HTTP URL is recognized.
3. Checking whether a non-HTTP URL is rejected.
4. Removing quotation marks from a string.
5. Checking string truncation.
6. Formatting a date with leading zeros.
7. Extracting a filename from a URL.
8. Converting an IPv4-mapped IPv6 address into an IPv4 address.

### How to Run the Tests

Make sure the project dependencies are installed.

**Run the complete unit test suite:**

```
npx vitest run tests/unit/utils.unit.test.ts
```

The test cases were first executed individually to check their results. After that, all 8 test cases were run together as one complete test suite.

**Test Results**

- Total test cases: 8
- Individual test executions: 8 passed
- Complete test suite: 8 passed
- Failed: 0
- Skipped: 0
- Execution rate: 100%
- Pass rate: 100%
- Complete suite duration: 382 ms
- Test-file execution time: 11 ms

The individual test results and the complete suite execution were recorded. Supporting screenshots are available in the evidence/ and test-results/ directories.

## **3.Integration Testing**

### Overview

Integration testing was performed on the OWASP Juice Shop application to check whether different parts of the application were working properly together. The tests focused on payment card operations, checkout, order history, and handling invalid payment information.

### Tools Used

- Python 3.14.2
- pytest 9.2.0
- Requests
- GitHub Codespaces

### Test Cases

A total of 4 integration test cases were created. They covered:

1. Creating a payment card and checking whether its information could be retrieved.
2. Completing a checkout and verifying the order history.
3. Checking whether the application rejects an invalid payment card.
4. Deleting a payment card and checking whether it was successfully removed.

### How to Run the Tests

Make sure the required libraries are installed:

```
pip install pytest requests
```

Start the OWASP Juice Shop application and make sure it is running at:

<http://localhost:3000>

**Run the complete integration test suite:**

```
pytest tests/integration/ -v
```

The test cases were first executed individually to check their results. After that, all 4 test cases were run together as one complete test suite.

### Test Results

- Total test cases: 4
- Individual test executions: 4 passed
- Complete test suite: 4 passed
- Failed: 0
- Blocked: 0
- Execution rate: 100%
- Pass rate: 100%
- Complete suite duration: 0.85 seconds

The individual test results and complete suite execution were recorded. Supporting screenshots and results are available in the evidence/ and test-results/ directories.

## 4.Selenium Testing

### Overview

I performed Selenium testing on the OWASP Juice Shop application to check some of its main features through automated browser testing. I used Python, Selenium WebDriver, and pytest to write and execute five test cases.

### Testing Environment

| **Component**        | **Details**                            |
| -------------------- | -------------------------------------- |
| Application          | OWASP Juice Shop                       |
| Framework            | Selenium WebDriver 4.53.0              |
| Programming Language | Python 3.14.2                          |
| Test Runner          | pytest 9.2.0                           |
| Browser              | Google Chrome 158.0.8127.36            |
| Browser Mode         | Headless                               |
| Environment          | GitHub Codespaces (Ubuntu 24.04.5 LTS) |

### Test Cases

I implemented the following five test cases:

1. SEL-01: Homepage Loads Successfully
2. SEL-02: Search for Apple Juice
3. SEL-03: Login with Invalid Credentials
4. SEL-04: Registration and Login Workflow
5. SEL-05: Add Product to Basket and Verify

### Installation and Setup

I installed Selenium and pytest using:

```
pip install pytest selenium
```

Before running the tests, I started the Juice Shop application:

```
npm start
```

### Test Execution

I first executed all five test cases individually to check their results. After confirming that each test passed, I ran all five together as a complete test suite.

**Individual Test Execution Commands**

**SEL-01 – Homepage Loads Successfully**

```
pytest tests/selenium/test_juice_shop_selenium.py::test_homepage_loads_successfully -v
```

**SEL-02 – Search for Apple Juice**

```
pytest tests/selenium/test_juice_shop_selenium.py::test_search_product -v
```

**SEL-03 – Login with Invalid Credentials**

```
pytest tests/selenium/test_juice_shop_selenium.py::test_login_with_invalid_credentials -v
```

**SEL-04 – Registration and Login Workflow**

```
pytest tests/selenium/test_juice_shop_selenium.py::test_registration_and_login_workflow -v
```

**SEL-05 – Add Product to Basket and Verify**

```
pytest tests/selenium/test_juice_shop_selenium.py::test_add_product_to_basket -v
```

**Full Test Suite Execution**

After completing the individual executions, I ran all five test cases together:

```
pytest tests/selenium/test_juice_shop_selenium.py -v
```

### Test Files

- tests/selenium/conftest.py – Contains the browser setup and Selenium fixture.
- tests/selenium/test_juice_shop_selenium.py – Contains all five Selenium test functions.

### Test Results

| **Description**                 | **Result**    |
| ------------------------------- | ------------- |
| Total Test Cases                | 5             |
| Individual Executions Passed    | 5             |
| Full Suite Passed               | 5             |
| Failed                          | 0             |
| Pass Rate                       | 100%          |
| Total Individual Execution Time | 59.60 seconds |
| Full Suite Execution Time       | 56.76 seconds |

All five test cases passed during individual execution and also passed when I ran them together as a complete test suite.

**5\. Playwright Testing**

**Overview**

I performed Playwright testing on the OWASP Juice Shop application to check some of its main features through automated browser testing. I used Python, Playwright, and pytest to write and execute five test cases.

**Testing Environment**

| **Component**        | **Details**           |
| -------------------- | --------------------- |
| Application          | OWASP Juice Shop      |
| Framework            | Playwright 1.65.2     |
| Programming Language | Python 3.14.2         |
| Test Runner          | pytest 9.2.0          |
| Browser              | Chromium 159.0.8154.6 |
| Browser Mode         | Headless              |
| Environment          | GitHub Codespaces     |

**Test Cases**

I implemented the following five test cases:

1. PW-01: Verify Product Details
2. PW-02: Verify Shopping Basket Opens
3. PW-03: Verify Login Form Validation
4. PW-04: Verify Navigation Menu
5. PW-05: Verify Product Search with No Matching Results

**Installation and Setup**

I installed Playwright and pytest using:

pip install pytest-playwright

I installed the Chromium browser using:

playwright install chromium

Before running the tests, I started the Juice Shop application:

npm start

**Test Execution**

I first executed all five test cases individually to check their results. After confirming that each test passed, I ran all five together as a complete test suite.

**Individual Test Execution Commands**

**PW-01 – Verify Product Details**

pytest tests/playwright/test_juice_shop_playwright.py::test_product_details -v

**PW-02 – Verify Shopping Basket Opens**

pytest tests/playwright/test_juice_shop_playwright.py::test_shopping_basket_opens -v

**PW-03 – Verify Login Form Validation**

pytest tests/playwright/test_juice_shop_playwright.py::test_login_form_validation -v

**PW-04 – Verify Navigation Menu**

pytest tests/playwright/test_juice_shop_playwright.py::test_navigation_menu -v

**PW-05 – Verify Product Search with No Matching Results**

pytest tests/playwright/test_juice_shop_playwright.py::test_product_search_no_matching_results -v

**Full Test Suite Execution**

After completing the individual executions, I ran all five test cases together:

pytest tests/playwright/test_juice_shop_playwright.py -v

**Test Files**

\- tests/playwright/test_juice_shop_playwright.py – Contains all five Playwright test functions.

**Test Results**

| **Description**                 | **Result**    |
| ------------------------------- | ------------- |
| Total Test Cases                | 5             |
| Individual Executions Passed    | 5             |
| Full Suite Passed               | 5             |
| Failed                          | 0             |
| Pass Rate                       | 100%          |
| Total Individual Execution Time | 18.73 seconds |
| Full Suite Execution Time       | 13.82 seconds |

All five test cases passed during individual execution and also passed when I ran them together as a complete test suite.

## 6. Non-Functional Testing

### Overview

Non-Functional Testing was performed on the OWASP Juice Shop application to check its performance and accessibility. The testing focused on page performance, server response time, accessibility issues, and keyboard navigation.

A total of five test cases (NFT-01 to NFT-05) were documented under two quality attributes: Performance and Accessibility.

### Tools Used

- Google Lighthouse
- Python
- Playwright
- Browser Developer Tools
- Chrome Browser
- JSON and CSV files for storing test results

### Test Cases

| **Test ID** | **Test Scenario**                                                                                         | **Quality Attribute** |
| ----------- | --------------------------------------------------------------------------------------------------------- | --------------------- |
| NFT-01      | Lighthouse performance score was 44/100.                                                                  | Performance           |
| NFT-02      | FCP: 0.7 s, LCP: 8.1 s, Speed Index: 4.6 s, TBT: 2,232 ms, CLS: 0.065.                                    | Performance           |
| NFT-03      | Lighthouse accessibility score was 87/100. Issues included accessible names, colour contrast, and labels. | Accessibility         |
| NFT-04      | Verify Keyboard Navigation and Accessibility of Interface Elements                                        | Accessibility         |
| NFT-05      | Verify Server Response Time Using Browser Navigation Timing API                                           | Performance           |

### Installation and Setup

The following tools and packages were used for Non-Functional Testing:

1. Python was used to execute the testing scripts.
2. Playwright was used for browser automation.
3. Chromium was installed for running the Playwright tests.
4. Google Lighthouse was used to check application performance and accessibility.
5. OWASP Juice Shop was started locally before running the tests.

Install the required Python packages if they are not already installed:

```
pip install pytest playwright
```

Install the Playwright Chromium browser:

```
playwright install chromium
```

Start the OWASP Juice Shop application:

```
npm start
```

The application was accessed locally at:

```
http://localhost:3000
```

### Test Execution

The following steps were followed to perform the Non-Functional Tests.

**NFT-01: Application Performance Using Lighthouse**

1. Open the OWASP Juice Shop application in Google Chrome.
2. Open Chrome Developer Tools.
3. Select the Lighthouse tab.
4. Run a performance audit.
5. Save the generated Lighthouse report and screenshot.

**NFT-02: Page Loading Speed and Core Web Vitals**

1. Review the Lighthouse performance results.
2. Check the First Contentful Paint (FCP), Largest Contentful Paint (LCP), Speed Index, Total Blocking Time (TBT), and Cumulative Layout Shift (CLS).
3. Record the measurements and save the results.

Note: NFT-01 and NFT-02 use the same Lighthouse performance audit and report. NFT-02 documents the page-loading and Core Web Vitals measurements from that audit; it was not a separate Lighthouse execution.

**NFT-03: Application Accessibility Using Lighthouse**

1. Open the application in Google Chrome.
2. Open Chrome Developer Tools and select the Lighthouse tab.
3. Run an accessibility audit.
4. Review the accessibility score and reported issues.
5. Save the Lighthouse report and screenshot.

**NFT-04: Keyboard Navigation and Accessibility**

The following Python scripts were used:

Run the keyboard navigation test:

```
python non_functional/nft04_keyboard_test.py
```

Run the dropdown accessibility test:

```
python non_functional/nft04_dropdown_test.py
```

These scripts were used to check keyboard navigation and dropdown interaction in the application. The generated results and screenshots were saved as evidence.

**NFT-05: Server Response Time Using Browser Navigation Timing API**

Run the Python test script:

```
python non_functional/nft05_server_response_test.py
```

The script opened the application using Playwright and collected five HTTP response measurements. It recorded the HTTP status code and Time to First Byte (TTFB), then generated JSON, CSV, and screenshot evidence.

### Test Results

| **Test ID** | **Actual Result**                                                                                         | **Status**                  |
| ----------- | --------------------------------------------------------------------------------------------------------- | --------------------------- |
| NFT-01      | Lighthouse performance score was 44/100.                                                                  | Needs Improvement           |
| NFT-02      | FCP: 0.7 s, LCP: 8.1 s, Speed Index: 4.6 s, TBT: 2,232 ms, CLS: 0.065.                                    | Needs Improvement           |
| NFT-03      | Lighthouse accessibility score was 87/100. Issues included accessible names, colour contrast, and labels. | Needs Improvement           |
| NFT-04      | Keyboard navigation and dropdown interactions were tested successfully, with some observations.           | Completed with Observations |
| NFT-05      | All 5 requests returned HTTP 200. Average TTFB was 25.24ms.                                               | Completed with Observations |

### Test Execution Summary

| **Metric**                  | **Result**     |
| --------------------------- | -------------- |
| Total Documented Test Cases | 5              |
| Total Executed Test Cases   | 5              |
| Needs Improvement           | 3              |
| Completed with Observations | 2              |
| Blocked Test Cases          | 0              |
| Execution Rate              | 100%           |
| Pass Rate                   | Not Calculated |

### Additional Observations

- NFT-01 and NFT-02 describe different aspects of the same Lighthouse performance audit. They should not be considered two independent Lighthouse executions.
- The Lighthouse performance audit identified areas where application performance could be improved.
- The accessibility audit identified issues related to accessible names, colour contrast, and labels.
- The keyboard tests showed that the main navigation and dropdown interactions could be performed using the keyboard.
- NFT-05 measured browser-observed TTFB over five requests. These measurements do not represent a full load or stress test, and TTFB is not a measurement of backend processing time alone.

### Test Evidence

The following evidence files were collected during testing:

- lighthouse-performance.html
- lighthouse-accessibility.html
- NFT-01_NFT-02_Performance_Results.png
- NFT-03_Accessibility_Result.png
- NFT-04_Keyboard_Navigation.png
- NFT-04_Keyboard_Dropdown_Test.png
- nft04_keyboard_results.json
- nft04_keyboard_test.py
- nft04_dropdown_test.py
- NFT-05_Server_Response_Results.png
- nft05_server_response_test.py
- nft05_response_results.json
- nft05_response_summary.csv

### Defect Summary

During API testing, two registration-validation defects were identified and recorded in the defect register:

1. The application accepted an invalid email address.
2. The application accepted a very short password.

DEF-01 (invalid email accepted) is provisionally Medium severity/priority, and DEF-02 (three-character password accepted) is provisionally High severity/priority. Both remain open and have not been fixed or retested. No other defects were recorded in the results of the remaining testing categories.