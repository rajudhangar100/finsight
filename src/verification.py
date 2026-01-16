from intent_infer import predict_intent

queries = [
    "Can employer deduct PF contribution from salary?",
    "Is EPF mandatory for employees?",
    "What are ESIC contribution rates?"
]

for q in queries:
    intent, conf = predict_intent(q)
    print(q, "→", intent, conf)
