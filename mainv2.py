#!/usr/bin/env python
# coding: utf-8
"""
Reddit Sentiment Analysis Tool for WallStreetBets
Analyzes sentiment of comments about specific stocks from r/wallstreetbets
and saves the results to a CSV file.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import praw
import pandas as pd
import datetime as dt
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Download required NLTK data
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Reddit API configuration
REDDIT_CONFIG = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT')
}

# Initialize Reddit client
reddit = praw.Reddit(**REDDIT_CONFIG)

# Target subreddit and stocks to analyze
SUBREDDIT_NAME = 'wallstreetbets'
STOCKS = ["GME", "AMC"]

# Create output directory for visualizations
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)

def get_sentiment_analyzer() -> SIA:
    """Initialize and return the VADER sentiment analyzer."""
    return SIA()

def analyze_comment_sentiment(comment: str, sia: SIA) -> Dict[str, Any]:
    """
    Analyze the sentiment of a single comment.
    
    Args:
        comment: The comment text to analyze
        sia: VADER sentiment analyzer instance
    
    Returns:
        Dictionary containing sentiment scores and the original comment
    """
    scores = sia.polarity_scores(comment)
    scores['headline'] = comment
    return scores

def get_comment_sentiment_average(comments: List[str]) -> float:
    """
    Calculate the average sentiment score for a list of comments.
    
    Args:
        comments: List of comment texts
    
    Returns:
        Average sentiment score (0 if no valid comments)
    """
    if not comments:
        return 0.0
        
    sia = get_sentiment_analyzer()
    results = [analyze_comment_sentiment(comment, sia) for comment in comments]
    
    df = pd.DataFrame.from_records(results)
    df['label'] = 0
    
    try:
        df.loc[df['compound'] > 0.1, 'label'] = 1
        df.loc[df['compound'] < -0.1, 'label'] = -1
    except:
        return 0.0
    
    return df['label'].mean()

def get_latest_comment_date(submission_url: str) -> Optional[float]:
    """
    Get the timestamp of the latest comment in a submission.
    
    Args:
        submission_url: URL of the Reddit submission
    
    Returns:
        Unix timestamp of the latest comment, or None if no comments
    """
    try:
        submission = reddit.submission(url=submission_url)
        comment_dates = [comment.created_utc for comment in submission.comments]
        return max(comment_dates) if comment_dates else None
    except:
        return None

def get_submission_comments(submission_url: str) -> List[str]:
    """
    Extract all comments from a submission.
    
    Args:
        submission_url: URL of the Reddit submission
    
    Returns:
        List of comment texts
    """
    try:
        submission = reddit.submission(url=submission_url)
        return [comment.body for comment in submission.comments]
    except:
        return []

def convert_timestamp(timestamp: float) -> dt.datetime:
    """Convert Unix timestamp to datetime object."""
    return dt.datetime.fromtimestamp(timestamp)

def collect_submission_statistics() -> pd.DataFrame:
    """
    Collect statistics about submissions for each stock.
    
    Returns:
        DataFrame containing submission statistics
    """
    submission_stats = []
    
    for ticker in STOCKS:
        for submission in reddit.subreddit(SUBREDDIT_NAME).search(ticker, limit=130):
            if submission.domain != "self.wallstreetbets":
                continue
                
            comments = get_submission_comments(submission.url)
            sentiment_avg = get_comment_sentiment_average(comments)
            
            if sentiment_avg == 0.0:
                continue
                
            stats = {
                'ticker': ticker,
                'num_comments': submission.num_comments,
                'comment_sentiment_average': sentiment_avg,
                'latest_comment_date': get_latest_comment_date(submission.url),
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'date': submission.created_utc,
                'domain': submission.domain,
                'num_crossposts': submission.num_crossposts,
                'author': submission.author
            }
            submission_stats.append(stats)
    
    df = pd.DataFrame(submission_stats)
    
    # Add datetime columns
    df['timestamp'] = df['date'].apply(convert_timestamp)
    df['commentdate'] = df['latest_comment_date'].apply(convert_timestamp)
    
    # Sort by latest comment date
    df.sort_values("latest_comment_date", axis=0, ascending=True, inplace=True, na_position='last')
    
    return df

# def create_visualizations(df: pd.DataFrame) -> None:
#     """
#     Create and save various visualizations of the sentiment analysis results.
    
#     Args:
#         df: DataFrame containing the sentiment analysis results
#     """
#     # Set style for all plots
#     plt.style.use('seaborn-v0_8')  # Updated style name
    
#     # 1. Sentiment Distribution by Stock
#     plt.figure(figsize=(10, 6))
#     sns.boxplot(x='ticker', y='comment_sentiment_average', data=df)
#     plt.title('Sentiment Distribution by Stock')
#     plt.xlabel('Stock Ticker')
#     plt.ylabel('Average Sentiment Score')
#     plt.savefig(OUTPUT_DIR / 'sentiment_by_stock.png')
#     plt.close()
    
#     # 2. Sentiment Over Time
#     plt.figure(figsize=(12, 6))
#     for ticker in STOCKS:
#         ticker_data = df[df['ticker'] == ticker]
#         plt.plot(ticker_data['timestamp'], 
#                 ticker_data['comment_sentiment_average'], 
#                 label=ticker, 
#                 marker='o', 
#                 markersize=4)
#     plt.title('Sentiment Trends Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Average Sentiment Score')
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.savefig(OUTPUT_DIR / 'sentiment_over_time.png')
#     plt.close()
    
#     # 3. Post Engagement vs Sentiment
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(data=df, 
#                    x='comment_sentiment_average', 
#                    y='num_comments',
#                    hue='ticker',
#                    alpha=0.6)
#     plt.title('Post Engagement vs Sentiment')
#     plt.xlabel('Average Sentiment Score')
#     plt.ylabel('Number of Comments')
#     plt.savefig(OUTPUT_DIR / 'engagement_vs_sentiment.png')
#     plt.close()
    
#     # 4. Upvote Ratio vs Sentiment
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(data=df, 
#                    x='comment_sentiment_average', 
#                    y='upvote_ratio',
#                    hue='ticker',
#                    alpha=0.6)
#     plt.title('Upvote Ratio vs Sentiment')
#     plt.xlabel('Average Sentiment Score')
#     plt.ylabel('Upvote Ratio')
#     plt.savefig(OUTPUT_DIR / 'upvotes_vs_sentiment.png')
#     plt.close()

def main():
    """Main execution function."""
    df = collect_submission_statistics()
    
    # Print author statistics
    print("\nAuthor Statistics:")
    print(df.author.value_counts())
    
    # Create visualizations
    print("\nCreating visualizations...")
    create_visualizations(df)
    print(f"Visualizations saved to {OUTPUT_DIR} directory")
    
    # Save results to CSV
    df.to_csv('Reddit_Sentiment_Equity.csv', index=False)
    print("\nResults saved to Reddit_Sentiment_Equity.csv")

if __name__ == "__main__":
    main() 