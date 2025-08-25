import pandas as pd
import ast

# Load the categorized comments
df = pd.read_csv("llm_categorized_comments.csv")

# Parse stringified list of categories
def parse_categories(cell):
    try:
        return ast.literal_eval(cell)
    except:
        return []

df["parsed_categories"] = df["llm_category"].apply(parse_categories)

# Flatten and count
all_categories = [cat for sublist in df["parsed_categories"] for cat in sublist]
llmcount = pd.Series(all_categories).value_counts().reset_index()
llmcount.columns = ["category", "count"]

# Save for reuse
llmcount.to_csv("category_counts.csv", index=False)
print(llmcount)
