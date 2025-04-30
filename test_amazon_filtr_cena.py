import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        yield browser
        browser.close()

@pytest.fixture(scope="module")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_search_functionality(page):
    page.goto("https://www.amazon.de")
    
    # Počkejme na vyhledávací pole, aby se načetlo
    page.wait_for_selector('input#twotabsearchtextbox', timeout=10000)  # čekání 10 sekund
    
    # Vyplnění vyhledávacího pole
    search_bar = page.query_selector('input#twotabsearchtextbox')
    search_bar.fill("laptop")
    
    # Kliknutí na tlačítko pro hledání
    search_button = page.query_selector('input#nav-search-submit-button')
    search_button.click()

    # Čekání na načtení výsledků
    page.wait_for_selector(".s-main-slot .s-result-item", timeout=10000)

    # Ověření, že se na stránce objevily výsledky
    results = page.query_selector_all(".s-main-slot .s-result-item")
    assert len(results) > 0, "Nenalezeny žádné výsledky pro hledaný termín."

def test_sort_by_price(page):
    page.goto("https://www.amazon.de")
    
    # Počkejme na vyhledávací pole, aby se načetlo
    page.wait_for_selector('input#twotabsearchtextbox', timeout=10000)  # čekání 10 sekund
    
    # Vyplnění vyhledávacího pole
    search_bar = page.query_selector('input#twotabsearchtextbox')
    search_bar.fill("laptop")
    
    # Kliknutí na tlačítko pro hledání
    search_button = page.query_selector('input#nav-search-submit-button')
    search_button.click()