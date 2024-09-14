import os
from data_utils import read_data
from tweet_gen import generate_tweet
from image_gen import save_chat_bubble_image
from datetime import datetime


def generate_all_tweets(df):
    os.makedirs("Britain/tweets", exist_ok=True)
    os.makedirs("Britain/images", exist_ok=True)

    with open("Britain/tweets/tweets.txt", "w", encoding="utf-8") as f:
        for index, row in df.iterrows():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tweet = generate_tweet(row)
            if tweet is not None:
                # Save tweet
                f.write(f"{tweet}\n\n\n")

                # Save image
                image_path = f"Britain/images/tweet_{index}.png"
                save_chat_bubble_image(tweet, image_path)
                print(
                    f"[{current_time}] Generated tweet and image for position {index} out of {len(df)}"
                )
            else:
                print(
                    f"[{current_time}] Failed to generate tweet for position {index} out of {len(df)}"
                )


if __name__ == "__main__":
    df = read_data()
    generate_all_tweets(df)
    print("All tweets and images have been generated and saved")
