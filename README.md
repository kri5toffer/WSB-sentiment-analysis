# Reddit Sentiment Analysis Tool

This tool analyzes sentiment of comments about specific stocks from r/wallstreetbets using Natural Language Processing (NLP) techniques. It helps understand market sentiment by analyzing how Reddit users feel about particular stocks.

## What is Sentiment Analysis?

Sentiment Analysis is a Natural Language Processing (NLP) technique that determines the emotional tone behind a piece of text. In this project, we use VADER (Valence Aware Dictionary and sEntiment Reasoner), which is specifically attuned to sentiments expressed in social media.

### How VADER Sentiment Analysis Works:

1. **Dictionary-based Approach**: VADER uses a lexicon of words rated for their sentiment intensity
2. **Polarity Scores**: For each text, it provides four metrics:
   - `compound`: Overall sentiment score (normalized between -1 and 1)
   - `pos`: Positive sentiment score
   - `neu`: Neutral sentiment score
   - `neg`: Negative sentiment score
3. **Social Media Awareness**: VADER is specifically tuned to understand:
   - Emoticons (e.g., :), :(, :-))
   - Acronyms (e.g., LOL, ROFL)
   - Punctuation (e.g., "Great!!!" vs "Great")
   - Capitalization (e.g., "GREAT" vs "great")

Set up Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Click "create app" or "create another app"
   - Note down your client ID and client secret

Update the `REDDIT_CONFIG` with your credentials:
```python
REDDIT_CONFIG = {
    'client_id': "YOUR_CLIENT_ID",
    'client_secret': "YOUR_CLIENT_SECRET",
    'user_agent': 'YOUR_APP_NAME'
}
```

## Output

The script generates several files:

1. **Reddit_Sentiment_Equity.csv**: Contains all analyzed data including:
   - Stock ticker
   - Number of comments
   - Average sentiment score
   - Latest comment date
   - Post score and upvote ratio
   - Author information

## Interpreting Results

- **Sentiment Scores**:
  - Positive values (> 0): Positive sentiment
  - Negative values (< 0): Negative sentiment
  - Values near 0: Neutral sentiment
