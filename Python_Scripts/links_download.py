# Purpose: Download all links from a website and save to a text file.
# Quote: "Collect links like treasures."

import requests
from bs4 import BeautifulSoup

# Replace this with your target URL
url = "https://www.mgeko.cc/manga/return-of-the-disaster-class-hero-mg1/all-chapters/"

# Send a GET request
response = requests.get(url)
response.raise_for_status()  # Raise error if the request failed

# Parse HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all <a> tags with href attribute
links = []
for a_tag in soup.find_all("a", href=True):
    link = a_tag["href"]
    links.append(link)

# Save links to a file
with open("links.txt", "w") as file:
    for link in links:
        file.write(link + "\n")

print(f"Found {len(links)} links. Saved to links.txt")
