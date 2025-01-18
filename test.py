import os
from dotenv import load_dotenv
import random
import tweepy
import time
from time import sleep
import openai
import schedule
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()

# API keys from .env
API_KEY = os.getenv('TwitterKey')
API_SECRET_KEY = os.getenv('TwitterSecret')
ACCESS_TOKEN = os.getenv('TwitterAccessToken')
ACCESS_SECRET = os.getenv('TwitterAccessSecret')
# OpenAI API Key
openai.api_key = os.getenv("OpenAiKey")

# Authenticate with the Twitter API using Tweepy
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Define Donald J. Trumpeeto's personality

personality = {

    "name": "Donald J. Trumpeeto",
    "obsession": "Cheetos",
    "traits": [
        "Bombastic and over-the-top",
        "Constantly self-promoting",
        "Obsessively loyal to Cheetos",
        "Dismissive of other snacks as 'losers'",
        "Uses hyperbolic language like 'the greatest snack ever made'",
        "Playfully arrogant, but charismatic",
        "Occasionally refers to himself as the 'snack king'"
    ],

    "motto": "Make snacking great again, one Cheeto at a time!"
}

# Generate dynamic content using GPT

def generate_response(prompt):
    try:
        response = openai.chat.completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.8
        )

        return response.choices[0].text.strip()

    except Exception as e:

        print(f"Error generating response: {e}")

        return "Folks, Cheetos are the greatest snack. Believe me!"

# Post a tweet

def post_tweet():

    prompt = f"Generate a tweet in the voice of {personality['name']}, who is obsessed with {personality['obsession']}. The tweet should reflect these traits: {', '.join(personality['traits'])}. It should be bombastic, funny, and self-promotional."
    tweet = generate_response(prompt)

    try:
        api.update_status(tweet)
        print(f"Posted tweet: {tweet}")

    except Exception as e:

        print(f"Error posting tweet: {e}")

# Reply to mentions dynamically

def reply_to_mentions():

    print("Checking for mentions...")
    mentions = api.mentions_timeline(count=10)
    for mention in mentions:
        if not mention.favorited:  # Skip already replied mentions
            try:
                prompt = f"Reply to a tweet from @{mention.user.screen_name} about Cheetos, in the voice of {personality['name']}. Reflect these traits: {', '.join(personality['traits'])}. Make it humorous and self-promotional."
                reply = generate_response(prompt)
                api.update_status(
                    f"@{mention.user.screen_name} {reply}",
                    in_reply_to_status_id=mention.id
                )

                api.create_favorite(mention.id)  # Mark as replied

                print(f"Replied to @{mention.user.screen_name}")

            except Exception as e:

                print(f"Error replying to mention: {e}")

# Search for tweets about Cheetos and reply dynamically

def search_and_reply():

    print("Searching for tweets to engage with...")

    tweets = api.search(q="Meme Coins", count=5, lang="en")

    for tweet in tweets:

        if not tweet.favorited:  # Skip already replied tweets

            try:

                prompt = f"Reply to a tweet about Cheetos, in the voice of {personality['name']}, who believes Cheetos are the greatest snack ever made. Make it playful, humorous, and self-promotional."
                reply = generate_response(prompt)
                api.update_status(
                    f"@{tweet.user.screen_name} {reply}",
                    in_reply_to_status_id=tweet.id
                )

                api.create_favorite(tweet.id)  # Mark as replied

                print(f"Engaged with tweet by @{tweet.user.screen_name}")

            except Exception as e:

                print(f"Error engaging with tweet: {e}")

# # Main loop for posting tweets and replying
# def main():
#     while True:
#         try:
#             tweet = post_tweet()
#             api.update_status(tweet)
#             print(f"Tweeted: {tweet}")
#             search_and_reply()
#             sleep(7000)  # Wait approximately 1.5 hours between posts
#         except tweepy.TweepError as e:
#             print(f"Error: {e}")
#             sleep(60)  # Wait 1 minute before retrying
#         except KeyboardInterrupt:
#             print("Stopping the bot.")
#             break



def job():
    print("Job is running!")

# Schedule the job
schedule.every(5).seconds.do(job)

# Function to check the next job's time
def get_next_scheduled_time():
    next_job = schedule.get_jobs()[0]  # Get the first job (or adjust if you have multiple jobs)
    return next_job.next_run

post_tweet()

# Schedule tasks

schedule.every(2).hours.do(post_tweet)
print("Scheduled task to post tweet every 2 hours")

schedule.every(15).minutes.do(reply_to_mentions)
print("Scheduled task to reply to mentions every 15 minutes")


schedule.every(30).minutes.do(search_and_reply)

print(f"{personality['name']} bot is running. Press Ctrl+C to stop.")

while True:

    schedule.run_pending()

    time.sleep(1)