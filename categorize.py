import pandas as pd
from collections import Counter

df = pd.read_csv("cleaned_comments.csv")

pain_categories = {
    "wrist pain": ["wrist", "carpal", "tunnel", "repetitive", "strain"],
    "hand pain": ["hand", "thumb", "finger", "grip"],
    "arm/shoulder pain": ["arm", "shoulder", "upper arm", "elbow"],
    "general fatigue": ["tired", "fatigue", "exhausted", "burnt out"],
    "cramps/soreness": ["cramp", "sore", "ache", "hurts", "hurt", "numb"],
    "tendonitis": ["tendonitis", "tendinitis"],
    "burnout/mental": ["burnout", "mentally", "overwhelmed", "stress", "anxiety"]
    # CTS - 
    # fingers and thumb instead of hand
    # pain -> ache/hurt
    # cramps -> sore/cramps/
}

def get_pain_category(comment, categories_dict):
    matched = []
    if not isinstance(comment, str):
        return matched
    
    comment = comment.lower()
    for category, keywords in categories_dict.items():
        if any(keyword in comment for keyword in keywords):
            matched.append(category)
    return matched

df["pain_categories"] = df["comment"].apply(lambda x: get_pain_category(x, pain_categories))

all_categories = sum(df["pain_categories"], [])

category_counts = Counter(all_categories)
category_summary = pd.DataFrame(category_counts.items(), columns=["Category", "Count"])
category_summary = category_summary.sort_values(by="Count", ascending=False)

category_summary.to_csv("categorized_counts.csv", index=False)
print("Done! Category counts saved to 'categorized_counts.csv'")

# Optional preview in terminal
print("\nTop categories:")
print(category_summary.head())



