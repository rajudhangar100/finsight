import spacy

nlp = spacy.load("models/ner_model")

doc = nlp("GST registration for paint shop in Karnataka")

for ent in doc.ents:
    print(ent.text, ent.label_)
