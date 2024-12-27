import time
import random
import asyncio
import json
import csv
from playwright.async_api import async_playwright

# List of random user-agents to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
]

# Randomized delay function
def random_delay():
    delay = random.uniform(5, 10)  # Increased delay to avoid detection
    time.sleep(delay)

async def scrape_elon_musk_profile():
    async with async_playwright() as p:
        # Randomly select a user agent
        random_agent = random.choice(user_agents)

        # Launch browser with randomized user-agent (without proxy)
        browser = await p.chromium.launch(
            headless=False,
            args=[f'--user-agent={random_agent}', '--no-sandbox', '--disable-gpu']
        )
        page = await browser.new_page()

        # Optional: Load cookies from a previous session (to avoid login)
        cookies = []  # Replace with actual cookies from a previous session if available
        try:
            with open('cookies.json', 'r') as f:
                cookies = json.load(f)
            if cookies:
                await page.context.add_cookies(cookies)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # No cookies found, will handle login if needed

        # Navigate to Elon Musk's public profile
        url = 'https://x.com/elonmusk'
        await page.goto(url)

        # Wait for the page to load
        try:
            await page.wait_for_selector('article', timeout=10000)  # 10 seconds timeout
        except:
            print("Timeout waiting for article selector, retrying...")
            await browser.close()
            return

        # Scrolling to load more tweets
        for _ in range(3):  # Scroll 3 times, adjust if necessary
            await page.mouse.wheel(0, 1000)
            random_delay()  # Wait for new tweets to load

        # Extract all tweets (post details)
        tweets = await page.query_selector_all('article')

        tweet_data = []
        for tweet in tweets:
            tweet_text = await tweet.inner_text()
            timestamp = await tweet.query_selector('time')
            likes = await tweet.query_selector('[data-testid="like"]')
            retweets = await tweet.query_selector('[data-testid="retweet"]')
            replies = await tweet.query_selector('[data-testid="reply"]')

            tweet_details = {
                'tweet_text': tweet_text.strip(),
                'timestamp': await timestamp.get_attribute('datetime') if timestamp else 'N/A',
                'likes': await likes.inner_text() if likes else '0',
                'retweets': await retweets.inner_text() if retweets else '0',
                'replies': await replies.inner_text() if replies else '0',
            }
            tweet_data.append(tweet_details)

        # Now scrape comments (replies) for each tweet
        comments_data = []
        for tweet in tweets:
            comment_button = await tweet.query_selector('[data-testid="reply"]')
            if comment_button:
                # Wait for the comment button to be fully visible and attached to the DOM
                try:
                    await page.wait_for_selector('[data-testid="reply"]:visible', timeout=5000)
                    if await comment_button.is_visible():
                        await comment_button.click()  # Click on the comment button to expand replies
                        await page.wait_for_timeout(3000)  # Wait for comments to load
                    else:
                        print("Comment button not visible, skipping...")
                except Exception as e:
                    print(f"Error while waiting for comment button: {e}")
                    continue

                # Extract comments for the tweet
                comments = await page.query_selector_all('[data-testid="tweetText"]')  # Comments' selectors
                for comment in comments:
                    comment_text = await comment.inner_text()
                    comment_author = await comment.query_selector('[dir="ltr"]')  # Get author info

                    comment_details = {
                        'comment_text': comment_text.strip(),
                        'author': await comment_author.inner_text() if comment_author else 'Unknown'
                    }
                    comments_data.append(comment_details)

        # Write the tweet and comment data to a CSV file
        with open('X_and_comments.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['tweet_text', 'timestamp', 'likes', 'retweets', 'replies', 'comment_text', 'comment_author']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Write tweets and comments
            for tweet in tweet_data:
                # If there are no comments, create a row with empty comment fields
                if not comments_data:
                    writer.writerow({
                        'tweet_text': tweet['tweet_text'],
                        'timestamp': tweet['timestamp'],
                        'likes': tweet['likes'],
                        'retweets': tweet['retweets'],
                        'replies': tweet['replies'],
                        'comment_text': 'N/A',
                        'comment_author': 'N/A'
                    })
                else:
                    for comment in comments_data:
                        writer.writerow({
                            'tweet_text': tweet['tweet_text'],
                            'timestamp': tweet['timestamp'],
                            'likes': tweet['likes'],
                            'retweets': tweet['retweets'],
                            'replies': tweet['replies'],
                            'comment_text': comment['comment_text'],
                            'comment_author': comment['author']
                        })

        # Save cookies after scraping (for future use)
        cookies = await page.context.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)

        # Close the browser
        await browser.close()

# Run the async function
asyncio.run(scrape_elon_musk_profile())
