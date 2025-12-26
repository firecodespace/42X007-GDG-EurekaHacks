from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://devpost.com", timeout=60000)

    print(">>> Log in manually in the opened browser.")
    print(">>> After you see yourself logged in, press ENTER here.")
    input()

    context.storage_state(path="storage_state.json")
    print(">>> storage_state.json saved successfully.")

    browser.close()
