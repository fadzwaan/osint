import requests
from bs4 import BeautifulSoup

URL = "https://division.iium.edu.my/"
RESULT_FILE = "result.txt"

response = requests.get(URL, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Select h3 elements that have the class directly
h3_elements = soup.find_all("h3", class_="elementskit-info-box-title")

texts = [h3.get_text(strip=True) for h3 in h3_elements]

# Write to result.txt
with open(RESULT_FILE, "w", encoding="utf-8") as f:
    for t in texts:
        f.write(t + "\n")

print(f"Extracted {len(texts)} items.")
print("Saved to result.txt")
