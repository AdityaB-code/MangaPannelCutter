# Purpose: Fast download without Selenium, just requests + BeautifulSoup.

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# === Get save folder from user ===
base_output = input("Enter FULL PATH to save chapters: ").strip()
if not os.path.isabs(base_output):
    print("❌ Please use an absolute path.")
    exit(1)

os.makedirs(base_output, exist_ok=True)

# === Read links ===
with open("few_downloadable_links.txt", "r") as f:
    chapter_links = [line.strip() for line in f if line.strip()]

# === Download loop ===
for idx, chapter_url in enumerate(chapter_links, start=1):
    print(f"\n📚 Chapter {idx}: {chapter_url}")

    chapter_name = f"chapter_{idx}"
    chapter_folder = os.path.join(base_output, chapter_name)
    os.makedirs(chapter_folder, exist_ok=True)

    try:
        r = requests.get(chapter_url, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to get {chapter_url}: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    img_tags = soup.find_all("img")
    img_count = 0

    for img_tag in img_tags:
        img_url = img_tag.get("src") or img_tag.get("data-src")
        if not img_url:
            continue

        img_url = urljoin(chapter_url, img_url)

        try:
            img_data = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20).content
        except Exception as e:
            print(f"❌ Could not download {img_url}: {e}")
            continue

        img_ext = os.path.splitext(urlparse(img_url).path)[1]
        if not img_ext:
            img_ext = ".jpg"

        img_name = f"image_{img_count+1:03d}{img_ext}"
        with open(os.path.join(chapter_folder, img_name), "wb") as f:
            f.write(img_data)
            img_count += 1

    print(f"✅ Saved {img_count} images in {chapter_folder}")

print("\n🎉 All done! (requests version)")
