import os
from bluesky_utils import post_to_bluesky


def post_tweets():
    with open("Britain/tweets/tweets.txt", "r", encoding="utf-8") as f:
        tweets = f.read().split("\n\n\n")

    for index, tweet in enumerate(tweets):
        if tweet.strip():
            image_path = f"Britain/images/tweet_{index}.png"
            if os.path.exists(image_path):
                post_to_bluesky(tweet, image_path)
                print(f"Posted tweet {index} to Bluesky")
            else:
                print(f"Image not found for tweet {index}")


if __name__ == "__main__":
    post_tweets()
    print("All tweets have been posted to Bluesky")
