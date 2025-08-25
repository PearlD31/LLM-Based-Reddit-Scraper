import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load cleaned comments
df = pd.read_csv("cleaned_comments.csv")

# Combine all comment text into one string
all_text = " ".join(str(comment) for comment in df["comment"] if pd.notnull(comment))

# Create the word cloud object
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis",  # you can change this to 'plasma', 'cool', 'rainbow', etc.
    max_words=200,
    collocations=False  # prevent "high pain" and "pain high" from doubling up
).generate(all_text)

# Display the word cloud
plt.figure(figsize=(15, 7.5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.show()
