from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/{1}")
    page.screenshot(path="example.png")
    browser.close()