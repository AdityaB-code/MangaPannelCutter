# Purpose: Make full links by adding base URL to relative links.

from urllib.parse import urljoin

BASE_URL = "https://www.mgeko.cc"
INPUT_FILE = "links.txt"
OUTPUT_FILE = "full_links.txt"

# Read relative links
with open(INPUT_FILE, "r") as f:
    relative_links = [line.strip() for line in f if line.strip()]

# Join with base URL
full_links = [urljoin(BASE_URL, rel) for rel in relative_links]

# Write full links to new file
with open(OUTPUT_FILE, "w") as f:
    for link in full_links:
        f.write(link + "\n")

print(f"Made {len(full_links)} full links → saved to {OUTPUT_FILE}")
