import re

LAWS = ["gst", "income tax", "pf", "esic"]
REGIONS = ["karnataka", "maharashtra", "india"]

def extract_entities(text):
    text_l = text.lower()

    law = next((l.upper() for l in LAWS if l in text_l), None)
    region = next((r.capitalize() for r in REGIONS if r in text_l), "India")

    return {
        "law": law,
    }
