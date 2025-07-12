# Purpose: Reverse the order of links in a text file.

# Read original links
with open("full_links.txt", "r") as f:
    links = [line.strip() for line in f if line.strip()]

# Reverse the list
links.reverse()

# Write to new file
with open("reversed_links.txt", "w") as f:
    for link in links:
        f.write(link + "\n")

print(f"Reversed {len(links)} links and saved to reversed_links.txt")
