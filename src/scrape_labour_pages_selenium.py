from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, os, json, re

URL = "https://www.epfindia.gov.in/site_en/FAQ.php"
OUTPUT_DIR = "data/knowledge/raw_docs/labour"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(URL)
time.sleep(4)

faq_data = []

panels = driver.find_elements(By.CSS_SELECTOR, ".panel.panel-default")

for panel in panels:
    try:
        # Question
        question_el = panel.find_element(By.CSS_SELECTOR, ".panel-heading a")
        question = clean(question_el.text)

        # Expand accordion
        driver.execute_script("arguments[0].click();", question_el)
        time.sleep(0.3)

        # Answer
        answer_el = panel.find_element(By.CSS_SELECTOR, ".panel-body")
        answer = clean(answer_el.text.replace("Ans :", ""))

        faq_data.append({
            "question": question,
            "answer": answer
        })

    except Exception:
        continue

driver.quit()

doc = {
    "title": "EPF Act FAQs",
    "url": URL,
    "law": "EPF Act",
    "intent": "LABOUR_LAW",
    "region": "India",
    "faqs": faq_data
}

with open(f"{OUTPUT_DIR}/EPF_Act.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"✅ Scraped {len(faq_data)} EPF FAQs correctly")
