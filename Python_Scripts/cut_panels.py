# Purpose: Robust panel splitter inspired by Manga-Panel-Extractor.

import cv2
import numpy as np
import os
from pathlib import Path

BASE_DIR = "/home/aditya/Programming/Python/Manhava/Return_of_disaster_class_hero/"
OUTPUT_DIR = "/home/aditya/Programming/Python/Manhava/Panels/"
MIN_PANEL_AREA = 5000  # Filter out tiny panels

os.makedirs(OUTPUT_DIR, exist_ok=True)

for chapter in os.listdir(BASE_DIR):
    chapter_path = os.path.join(BASE_DIR, chapter)
    if not os.path.isdir(chapter_path):
        continue

    for filename in os.listdir(chapter_path):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue

        img_path = os.path.join(chapter_path, filename)
        image = cv2.imread(img_path)

        if image is None:
            print(f"❌ Cannot read {img_path}")
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        # Use morphology to connect text & lines, then find contours
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        panel_num = 1
        chapter_name = Path(chapter).stem.replace(" ", "_")
        image_name = Path(filename).stem

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w * h < MIN_PANEL_AREA:
                continue  # skip tiny blobs

            panel = image[y:y + h, x:x + w]
            out_name = f"{chapter_name}_{image_name}_panel{panel_num}.jpg"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            cv2.imwrite(out_path, panel)
            panel_num += 1

        print(f"✅ {filename}: {panel_num-1} panels saved.")

print("\n🎉 All done: robust contour-based panels, no white padding.")
