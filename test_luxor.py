from playwright.sync_api import Page, expect

def test_homepage_and_books_navigation(page: Page):
    # Otevřu testovanou stránku: luxor.cz
    page.goto("https://www.luxor.cz")

    # Pomocí přesného selektoru "cmp-cookie-consent button.btn--primary" najdu tlačítko „Souhlasím“ uvnitř cookie banneru.
    # wait_for(state="visible") čeká, než bude tlačítko viditelné (a interaktivní). 
    # Kliknu na tlačítko. Pak čekám, až se celý element cookie lišty (cmp-cookie-consent) odstraní z DOMu 
    # (state="detached"), což je robustní způsob, jak zajistit, že banner opravdu zmizel.
    try:
        cookies_button = page.locator("cmp-cookie-consent button.btn--primary")
        cookies_button.wait_for(state="visible", timeout=10000)
        cookies_button.click()
        # Počkám, až cookie lišta úplně zmizí z DOMu
        page.locator("cmp-cookie-consent").wait_for(state="detached", timeout=10000)
    except:
        print("Cookie lišta se nezobrazila nebo už byla zavřená.")

    # Najdu a kliknu na odkaz „Knihy“ 
    knihy_link = page.locator("a.main-menu__link[href='/c/9548/knihy']")
    knihy_link.wait_for(state="visible", timeout=10000)
    # Ověřím, že odkaz je viditelný a interaktivní
    knihy_link.scroll_into_view_if_needed()
    knihy_link.click()

    # Počkám na načtení nové stránky
    page.wait_for_load_state("networkidle")

    # Ověřím, že se zobrazil nadpis HTML tagu h1 „Knihy“
    heading = page.locator("h1.category__title.heading-h1")
    heading.wait_for(state="visible", timeout=10000)
    expect(heading).to_have_text("Knihy")





  