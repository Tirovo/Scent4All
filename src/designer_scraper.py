import os
import asyncio
import csv
from playwright.async_api import async_playwright

# === Construction du chemin absolu vers le dossier "data/" à la racine ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # -> /Scent4All
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Crée le dossier s'il n'existe pas
OUTPUT_PATH = os.path.join(DATA_DIR, "designers.csv")

# === Reste du scraping ===
async def run():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto("https://www.fragrantica.fr/designer/")

        try:
            await page.locator("button:has-text('Accepter et fermer')").click()
            await page.wait_for_timeout(1000)
        except:
            print("Aucun bandeau cookie trouvé.")

        await page.wait_for_selector("div.designerlist")

        links = await page.query_selector_all("div.designerlist a")
        designers = []
        for link in links:
            name = (await link.inner_text()).strip()
            url = await link.get_attribute("href")
            if name and url:
                designers.append({"name": name, "url": "https://www.fragrantica.fr" + url})

        await browser.close()
        return designers

# === Main ===
if __name__ == '__main__':
    designers = asyncio.run(run())

    with open(OUTPUT_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url"])
        writer.writeheader()
        writer.writerows(designers)

    print(f"{len(designers)} designers sauvegardés dans '{OUTPUT_PATH}'")


