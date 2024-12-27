# Playwright Web Scraper 🧑‍💻🐍

## Overview 📋
The Playwright Web Scraper is an asynchronous Python script built using Playwright, designed to scrape content from websites such as Twitter (X) by navigating through posts, fetching comments, and interacting with dynamic web elements. This script includes features like rotating user agents, handling rate limits with randomized delays, and saving scraped data into a structured CSV file for analysis or further processing.

This scraper works by mimicking human-like browsing actions, which reduces the likelihood of being detected by websites as a bot.

## Why Use This? 🤔
This scraper can be useful for:

- **Data Analysis 📊**: Extracting social media content for analysis of trends, discussions, or behavior patterns.
- **Sentiment Analysis 💬**: Collecting posts and comments for sentiment analysis.
- **Research 📚**: Gathering data for academic studies or market research.
- **Content Aggregation 📑**: Scraping and aggregating posts and comments across multiple web pages.

## Features 🚀

- **Dynamic Content Scraping 📥**: Uses Playwright to interact with dynamic content, including clicking buttons and scrolling to load more posts or comments.
- **User-Agent Rotation 🔄**: Rotates between multiple user agents to avoid detection and minimize the chances of getting blocked.
- **Randomized Delays ⏳**: Introduces random delays between requests to mimic human browsing behavior and reduce bot detection.
- **Exponential Backoff for Rate Limiting 🚧**: Handles rate-limiting errors and retries failed requests without crashing the script.
- **Data Saving 💾**: Saves scraped posts and comments into a CSV file for further analysis.
- **Customizable ⚙️**: Easily configurable to target different web pages, interact with various elements, and modify scraping parameters.

## Sample Data 📋
The data is saved in a CSV file with the following structure:

```csv
tweet_text, timestamp, likes, retweets, replies, comment_text, comment_author
