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

## Features

- Analyzes Reddit comments about specified stocks
- Calculates sentiment scores for each comment
- Generates visualizations:
  - Sentiment distribution by stock
  - Sentiment trends over time
  - Post engagement vs sentiment
  - Upvote ratio vs sentiment
- Saves results to CSV for further analysis

## Prerequisites

- Python 3.7+
- Reddit API credentials (client ID and client secret)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd WSBRedditBot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Click "create app" or "create another app"
   - Fill in the required information
   - Select "script" as the app type
   - Note down your client ID and client secret

4. Update the `REDDIT_CONFIG` in the script with your credentials:
```python
REDDIT_CONFIG = {
    'client_id': "YOUR_CLIENT_ID",
    'client_secret': "YOUR_CLIENT_SECRET",
    'user_agent': 'YOUR_APP_NAME'
}
```

## Usage

1. Run the script:
```bash
python archive/tstewart161_main.py
```

2. The script will:
   - Fetch posts and comments from r/wallstreetbets
   - Analyze sentiment for each comment
   - Generate visualizations in the `output` directory
   - Save results to `Reddit_Sentiment_Equity.csv`

## Output

The script generates several files:

1. **Reddit_Sentiment_Equity.csv**: Contains all analyzed data including:
   - Stock ticker
   - Number of comments
   - Average sentiment score
   - Latest comment date
   - Post score and upvote ratio
   - Author information

2. **Visualizations** (in the `output` directory):
   - `sentiment_by_stock.png`: Box plot showing sentiment distribution for each stock
   - `sentiment_over_time.png`: Line plot showing sentiment trends over time
   - `engagement_vs_sentiment.png`: Scatter plot of post engagement vs sentiment
   - `upvotes_vs_sentiment.png`: Scatter plot of upvote ratio vs sentiment

## Interpreting Results

- **Sentiment Scores**:
  - Positive values (> 0): Positive sentiment
  - Negative values (< 0): Negative sentiment
  - Values near 0: Neutral sentiment

- **Visualizations**:
  - Higher sentiment scores indicate more positive discussion
  - Trends over time can show changing market sentiment
  - Correlation between engagement and sentiment can indicate community interest

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 