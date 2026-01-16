import requests
from bs4 import BeautifulSoup
import os, json, re, warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

INPUT_LINK_FILE = "data/knowledge/links/gst_registration_links.txt"
OUTPUT_DIR = "data/knowledge/raw_docs/gst_registration"

os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

with open(INPUT_LINK_FILE, "r", encoding="utf-8") as f:
    base_urls = [u.strip() for u in f if u.strip()]

for base_url in base_urls:
    try:
        # GST tutorial content lives in *1.htm
        content_url = base_url.replace(".htm", "1.htm")

        response = requests.get(content_url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(response.text, "lxml")

        body = soup.find("body")
        if not body:
            print(f"❌ No body: {content_url}")
            continue

        # Remove non-content tags
        for tag in body(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        text = clean_text(body.get_text(separator=" "))

        # 🔴 IMPORTANT: do NOT over-filter
        if len(text) < 200:
            print(f"⚠️ Still short (server limited): {content_url}")
            continue

        h1 = soup.find("h1")
        title = h1.get_text(strip=True) if h1 else base_url.split("/")[-1].replace(".htm", "")

        doc = {
            "title": title,
            "url": content_url,
            "law": "GST Act",
            "intent": "REGISTRATION",
            "region": "India",
            "text": text
        }

        filename = base_url.split("/")[-1].replace(".htm", ".json")

        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)

        print(f"✅ Scraped successfully: {title}")

    except Exception as e:
        print(f"❌ Error scraping {base_url}: {e}")
