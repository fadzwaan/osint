import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

URL = "https://division.iium.edu.my/finance/login/downloadable-forms/"
OUTPUT_DIR = "output"
RESULT_FILE = "result.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

session = requests.Session()
response = session.get(URL, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# ✅ ONLY anchors with this class
anchors = soup.find_all(
    "a",
    class_="dropdown-item menu-link",
    href=True
)

total_forms = len(anchors)
success = 0
failed = 0
details = []

for idx, a in enumerate(anchors, start=1):
    href = a["href"].strip()
    link = urljoin(URL, href)

    try:
        r = session.get(link, timeout=20, allow_redirects=True)

        # Google Drive access restriction
        if (
            "accounts.google.com" in r.url
            or "request access" in r.text.lower()
        ):
            raise Exception("Google Drive access restricted")

        # Must NOT be HTML
        content_type = r.headers.get("Content-Type", "").lower()
        if r.status_code != 200 or "text/html" in content_type:
            raise Exception("Not a downloadable file")

        filename = os.path.basename(urlparse(r.url).path)
        if not filename:
            filename = f"file_{idx}"

        path = os.path.join(OUTPUT_DIR, filename)

        with open(path, "wb") as f:
            f.write(r.content)

        success += 1
        details.append(f"[SUCCESS] {filename}")

    except Exception as e:
        failed += 1
        details.append(f"[FAILED] {link} | {str(e)}")

# Write result.txt
with open(RESULT_FILE, "w") as f:
    f.write(f"Total anchor forms : {total_forms}\n")
    f.write(f"Successfully downloaded : {success}\n")
    f.write(f"Failed downloads : {failed}\n\n")
    f.write(f"Public download form {success}/{total_forms}\n\n")
    f.write("Details:\n")
    for d in details:
        f.write(d + "\n")

print(f"Done. Public download form {success}/{total_forms}")
print("See result.txt for details.")
