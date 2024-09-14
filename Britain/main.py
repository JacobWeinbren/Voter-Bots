import os
from data_utils import read_data
from tweet_gen import generate_tweet
from image_gen import save_chat_bubble_image
from bluesky_utils import post_to_bluesky


def generate_and_save_single_tweet(df):
    os.makedirs("Britain/tweets", exist_ok=True)
    os.makedirs("Britain/images", exist_ok=True)

    # Read current position
    try:
        with open("Britain/current_position.txt", "r") as f:
            current_position = int(f.read().strip())
    except FileNotFoundError:
        current_position = 0

    # Generate tweet for the current position
    while current_position < len(df):
        row = df.iloc[current_position]
        tweet = generate_tweet(row)

        if tweet is not None:
            # Save tweet
            with open("Britain/tweets/tweets.txt", "a", encoding="utf-8") as f:
                f.write(f"{tweet}\n\n\n")

            # Save image
            image_path = f"Britain/images/tweet_{current_position}.png"
            save_chat_bubble_image(tweet, image_path)

            # Post to Bluesky
            post_to_bluesky(tweet, image_path)
            print(f"Posted tweet {current_position} to Bluesky")

            # Update current position
            current_position += 1
            with open("Britain/current_position.txt", "w") as f:
                f.write(str(current_position))
            break
        else:
            print(
                f"Failed to generate tweet for position {current_position}, trying next..."
            )
            current_position += 1

    if current_position >= len(df):
        print("All tweets have been generated or attempted")


if __name__ == "__main__":
    df = read_data()
    generate_and_save_single_tweet(df)
    print("Tweet has been generated, saved, and posted to Bluesky")
