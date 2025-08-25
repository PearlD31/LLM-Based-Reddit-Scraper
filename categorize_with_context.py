import pandas as pd
from collections import Counter

# Load your cleaned CSV that includes comment_id and parent_id
df = pd.read_csv("cleaned_comments.csv")

# Define the pain categories and associated keywords
pain_categories = {
    "wrist pain": ["wrist", "carpal", "tunnel", "repetitive", "strain"],
    "hand pain": ["hand", "thumb", "finger", "grip"],
    "arm/shoulder pain": ["arm", "shoulder", "upper arm", "elbow"],
    "general fatigue": ["tired", "fatigue", "exhausted", "burnt out"],
    "cramps/soreness": ["cramp", "sore", "ache", "hurts", "hurt", "numb"],
    "tendonitis": ["tendonitis", "tendinitis"],
    "burnout/mental": ["burnout", "mentally", "overwhelmed", "stress", "anxiety"]
}

# Function to match categories based on comment text
def get_pain_categories(comment, categories_dict):
    matched = []
    if not isinstance(comment, str):
        return matched
    comment = comment.lower()
    for category, keywords in categories_dict.items():
        if any(keyword in comment for keyword in keywords):
            matched.append(category)
    return matched

# Step 1: Tag direct matches
df["pain_categories"] = df["comment"].apply(lambda x: get_pain_categories(x, pain_categories))

# Step 2: Build a mapping of comment_id -> category
id_to_categories = dict(zip(df["comment_id"], df["pain_categories"]))

# Step 3: Inherit categories from parent if reply is blank
def inherit_categories(row):
    if row["pain_categories"]:  # direct match
        return row["pain_categories"]
    parent_id = row["parent_id"]
    return id_to_categories.get(parent_id, [])

# Step 4: Apply inheritance logic
df["final_categories"] = df.apply(inherit_categories, axis=1)

# Step 5: Count total occurrences of each category
all_final_categories = sum(df["final_categories"], [])
category_counts = Counter(all_final_categories)

# Step 6: Save category counts
category_summary = pd.DataFrame(category_counts.items(), columns=["Category", "Count"])
category_summary = category_summary.sort_values(by="Count", ascending=False)

# Save the full categorized data and summary counts
df.to_csv("categorized_with_context.csv", index=False)
category_summary.to_csv("categorized_counts_with_context.csv", index=False)

# Final status printout
print("Done! Context-aware categories saved to 'categorized_with_context.csv'")
print("Category counts saved to 'categorized_counts_with_context.csv'")
print("\nTop categories with context:")
print(category_summary.head())
