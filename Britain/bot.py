import os
from bluesky_utils import post_to_bluesky


def post_single_tweet():
    # Read the current position
    position_file = "Britain/current_position.txt"
    if os.path.exists(position_file):
        with open(position_file, "r") as f:
            current_position = int(f.read().strip())
    else:
        current_position = 0

    # Read all tweets
    with open("Britain/tweets/tweets.txt", "r", encoding="utf-8") as f:
        tweets = f.read().split("\n\n\n")

    # Post the next tweet if available
    if current_position < len(tweets):
        tweet = tweets[current_position].strip()
        if tweet:
            image_path = f"Britain/images/tweet_{current_position}.png"
            if os.path.exists(image_path):
                post_to_bluesky(tweet, image_path)
                print(f"Posted tweet {current_position} to Bluesky")
            else:
                print(f"Image not found for tweet {current_position}")

        # Update and save the new position
        current_position += 1
        with open(position_file, "w") as f:
            f.write(str(current_position))
    else:
        print("All tweets have been posted")


if __name__ == "__main__":
    post_single_tweet()
