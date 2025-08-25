import pandas as pd
df = pd.read_csv("comments.csv")

keywords = [ "pain", "hurt", "injury", "discomfort", "fatigue", "strain", "repetitive", "wrist", "tired", "cramp", "sore", "ache", "strain", "numb", "tendonitis"]

def is_relevant(comment):
    if pd.isnull(comment):
        return False
    comment = comment.lower()
    return any(keyword in comment for keyword in keywords)

filtered_df = df[df["comment"].apply(is_relevant)]
filtered_df.to_csv("filtered_comments.csv", index=False)

print(f"Filtered down to {len(filtered_df)} relevant comments!")
