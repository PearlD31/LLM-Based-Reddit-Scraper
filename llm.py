from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
import time
import os
import ast
import re
import asyncio
import httpx

load_dotenv()
client = OpenAI()

# Load dataset
df = pd.read_csv("cleaned_comments.csv")
df["llm_category"] = ""

# Define categories and keywords
categories = {
    "pain": ["wrist", "hand", "arm", "shoulder", "thumb", "finger", "grip", "ache", "cramp", "numb", "hurts", "hurt", "sore"],
    "strain": ["repetitive", "motion", "overuse", "intensity", "repetition", "high volume", "excessive use"],
    "fatigue": ["tired", "fatigue", "exhausted", "burnt out", "low energy"],
    "diagnosed disorders": ["tendonitis", "tendinitis", "arthritis", "carpal tunnel", "cts", "chronic", "syndrome"],
    "mental burnout": ["burnout", "mentally", "overwhelmed", "stress", "anxiety", "depression", "pressure", "emotional"],
    "postural issues": ["neck", "back", "posture", "ergonomics", "hunch", "slouch"],
    "tools and equipment": ["pipette", "pipetting", "equipment", "tool", "device", "manual", "broken", "design", "handle"],
    "environmental factors": ["lab", "lighting", "noise", "ventilation", "temperature", "workspace", "setup", "layout"],
    "workload and hours": ["hours", "long", "overtime", "schedule", "workload", "breaks", "rest", "time off"],
    "training and support": ["training", "guidance", "mentorship", "supervision", "learning", "instructions"]
}
valid_categories = [cat.lower() for cat in categories.keys()]

# Format for prompt
category_text = "\n".join([
    f"{cat}: {', '.join(keywords)}" for cat, keywords in categories.items()
])

# Normalize LLM output
def normalize_llm_response(text):
    text = text.strip().lower()

    # Handle empty/invalid responses
    if text in ["none", "no category", "n/a", "the", "n", "no match", "", "[]"]:
        return []

    # Extract list from brackets
    if "[" in text and "]" in text:
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if match:
            try:
                extracted = ast.literal_eval(match.group())
                return list(set([x.lower().strip() for x in extracted if x.lower().strip() in valid_categories]))
            except:
                pass

    # Single category
    if text.lower() in valid_categories:
        return [text.lower()]

    # Comma-separated string
    guesses = [x.strip(" '\"\n") for x in text.split(",")]
    cleaned = [g for g in guesses if g in valid_categories]
    return list(set(cleaned)) if cleaned else []

# Run LLM classification
for i, row in tqdm(df.iterrows(), total=len(df)):
    comment = row["comment"]

    prompt = f"""
You are analyzing Reddit comments from lab researchers describing their pain points and challenges with long-term pipetting.

Here are the categories and the types of keywords or symptoms they typically include:

{category_text}

Comment: "{comment}"

Which categories best match this comment? 
Respond ONLY with a list of category names from the list above. 
If none apply, respond with an empty list [].
""".strip()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful text classifier."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        raw = response.choices[0].message.content.strip()
        normalized = normalize_llm_response(raw)
        print(f" Row {i}: {normalized}")
        df.at[i, "llm_category"] = str(normalized)

        # Periodic backup
        if i % 20 == 0 and i > 0:
            df.to_csv("llm_categorized_comments_backup.csv", index=False)

    except Exception as e:
        print(f" Error on comment {i}: {comment[:60]}...\n{e}")
        df.at[i, "llm_category"] = "ERROR"
        time.sleep(1)

# Final save
df.to_csv("llm_categorized_comments.csv", index=False)
print("All done! Results saved to 'llm_categorized_comments.csv'")


#Calcuate accuracy, precision and recall


#Bubble Chart should be color-coded to iGEM design theme etc 