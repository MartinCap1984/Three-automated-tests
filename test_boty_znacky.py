import time
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize("znacka", ["Nike", "Reebok"])
def test_vyhledani_znacky(page: Page, znacka: str):
    page.goto("https://www.sportisimo.cz/", timeout=60000, wait_until="domcontentloaded")
    print(f"Aktualni URL: {page.url}")
    page.screenshot(path=f"debug_homepage_{znacka}.png")

    try:
        page.locator("#didomi-notice-agree-button").click(timeout=5000)
    except:
        print("Cookies tlačítko nebylo zobrazeno.")

    search_input = page.locator("#header_search_q")
    search_input.fill(znacka)
    search_input.press("Tab")
    search_input.press("Enter")

    page.wait_for_url("**/vyhledavani-produktu/**", timeout=15000)
    print(f"Načtena stránka výsledků: {page.url}")
    page.screenshot(path=f"debug_vysledky_{znacka}.png")

    znacka_locator = page.locator(f"text={znacka}")
    znacka_locator.first.wait_for(state="attached", timeout=20000)

    time.sleep(2)

    count = znacka_locator.count()
    print(f"Nalezeno výskytů '{znacka}': {count}")
    assert count > 0, f"Nebyly nalezeny žádné výskyty '{znacka}' ve stránce"
    expect(znacka_locator.first).to_have_text(re.compile(znacka, re.IGNORECASE))
