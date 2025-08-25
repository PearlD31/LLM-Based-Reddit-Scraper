import praw
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

reddit = praw.Reddit(
    client_id = client_id,
    client_secret = client_secret,
    user_agent= 'pipette-pain-analysis-nlp by /u/pea-irl')

print("Connected to Reddit API!")

keywords = [
    "pain", "hurt", "injury", "discomfort",
    "fatigue", "strain", "repetitive",
    "tired", "cramp", "sore", "ache", "numb",
    "tendonitis"
]

def is_relevant(text):
    if not text or not isinstance(text, str):
        return False
    text = text.lower()
    return any(keyword in text for keyword in keywords)

# load_dotenv(dotenv_path='/Users/pearl/igem-reddit-nlp/.env')

# client_id = os.getenv('CLIENT_ID')
# client_secret = os.getenv('CLIENT_SECRET')

subreddit = reddit.subreddit ('labrats')
posts = subreddit.search("pain OR fatigue OR repetitive OR strain OR injury OR discomfort", limit = 100)

all_comments = []
comment_lookup = {}

data = []

for post in posts:
    post.comments.replace_more (limit = 0)
    for comment in post.comments.list():
        comment_id = comment.id
        parent_id = comment.parent_id.split("_")[-1]

        comment_text = comment.body
        is_main_post = (comment.parent_id.startswith("t3"))

        comment_lookup[comment_id] = comment_text

        relevant = is_relevant(comment_text)

        short_reply = len(comment_text.strip()) < 15
        parent_comment = comment_lookup.get(parent_id, "")
        parent_relevant = is_relevant(parent_comment)

        
        if relevant or (short_reply and parent_relevant):
            all_comments.append({
                "post_title": post.title,
                "comment": comment_text,
                "score": comment.score,
                "post_url": post.url,
                "comment_id": comment_id,
                "parent_id": parent_id,
                "reply_to_relevant": short_reply and parent_relevant
            })

df = pd.DataFrame(all_comments)
df.to_csv("comments_with_context.csv", index=False)
print(f"Saved {len(df)} comments to comments.csv")

df = pd.read_csv("comments_with_context.csv")
def is_valid_comment(text):
    if not isinstance(text, str):
        return False
    text = text.lower().strip()
    return text not in ["[deleted]", "[removed]"] 

clean_df = df[df["comment"].apply(is_valid_comment)].copy()

clean_df.to_csv("cleaned_comments.csv", index=False)
print(f"Cleaned data saved! Now has {len(clean_df)} comments.")






