# Sentiment Analysis

This tool analyzes sentiment of comments about specific stocks from r/wallstreetbets using Natural Language Processing (NLP) techniques. It helps understand market sentiment by analyzing how Reddit users feel about particular stocks.

## What is Sentiment Analysis?

Sentiment Analysis is a Natural Language Processing (NLP) technique that determines the emotional tone behind a piece of text. In this project, we use VADER (Valence Aware Dictionary and sEntiment Reasoner), which is specifically attuned to sentiments expressed in social media.

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

**Reddit_Sentiment_Equity.csv**: Contains all analyzed data including:

**Sentiment Scores**:
  - Positive values (> 0): Positive sentiment
  - Negative values (< 0): Negative sentiment
  - Values near 0: Neutral sentiment
