from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, os, json, re

INPUT_LINK_FILE = "data/knowledge/links/gst_registration_links.txt"
OUTPUT_DIR = "data/knowledge/raw_docs/gst_registration"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

with open(INPUT_LINK_FILE, "r") as f:
    urls = [u.strip() for u in f if u.strip()]

for url in urls:
    try:
        driver.get(url)
        time.sleep(4)  # allow JS to load

        body = driver.find_element(By.TAG_NAME, "body")
        text = clean_text(body.text)

        if len(text) < 300:
            print(f"❌ Still empty: {url}")
            continue

        title = driver.title

        doc = {
            "title": title,
            "url": url,
            "law": "GST Act",
            "intent": "REGISTRATION",
            "region": "India",
            "text": text
        }

        filename = url.split("/")[-1].replace(".htm", ".json")

        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)

        print(f"✅ Scraped (JS rendered): {title}")

    except Exception as e:
        print(f"❌ Failed: {url} | {e}")

driver.quit()
