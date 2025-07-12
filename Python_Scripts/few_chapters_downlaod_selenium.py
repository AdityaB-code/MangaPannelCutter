# Purpose: Download manhwa images with Selenium & save to a user-specified folder.
# Quote: "Ask first, save smart."

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin, urlparse
import time

# === Ask user for save folder ===
base_output = input("Enter the FULL PATH where you want to save the chapters: ").strip()
if not os.path.isabs(base_output):
    print("❌ Please provide an absolute path!")
    exit(1)

os.makedirs(base_output, exist_ok=True)

# === Setup Selenium ===
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# === Read chapter links ===
with open("few_downloadable_links.txt", "r") as f:
    chapter_links = [line.strip() for line in f if line.strip()]

for idx, chapter_url in enumerate(chapter_links, start=1):
    print(f"\nProcessing chapter {idx}: {chapter_url}")

    # Create a subfolder for this chapter
    chapter_name = f"chapter_{idx}"
    chapter_folder = os.path.join(base_output, chapter_name)
    os.makedirs(chapter_folder, exist_ok=True)

    try:
        driver.get(chapter_url)
    except Exception as e:
        print(f"⚠️  Failed to open {chapter_url}: {e}")
        continue

    time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    img_tags = soup.find_all("img")
    img_count = 0

    for img_tag in img_tags:
        img_url = img_tag.get("src") or img_tag.get("data-src")
        if not img_url:
            continue

        img_url = urljoin(chapter_url, img_url)

        try:
            response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")
            continue

        img_ext = os.path.splitext(urlparse(img_url).path)[1]
        if not img_ext:
            img_ext = ".jpg"

        img_name = f"image_{img_count + 1:03d}{img_ext}"

        with open(os.path.join(chapter_folder, img_name), "wb") as f:
            f.write(response.content)
            img_count += 1

    print(f"✅ Downloaded {img_count} images for {chapter_name}")

driver.quit()
print("\n🎉 All done! Images organized properly.")
