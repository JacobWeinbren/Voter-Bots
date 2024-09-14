import os
from data_utils import read_data
from tweet_gen import generate_tweet
from image_gen import save_chat_bubble_image
from datetime import datetime
import numpy as np


def select_weighted_respondents(df):
    weights = df["wt_new_W29"].dropna()
    num_sample = len(weights)
    num_select = 365 * 4 * 5 * 8  # Eight is the approx buffer

    sample_indices = np.random.choice(
        weights.index, size=num_sample, replace=True, p=weights / weights.sum()
    )
    return set(np.random.choice(sample_indices, size=num_select, replace=False))


def generate_all_tweets(df):
    os.makedirs("Britain/tweets", exist_ok=True)
    os.makedirs("Britain/images", exist_ok=True)

    selected_indices = select_weighted_respondents(df)

    with open("Britain/tweets/tweets.txt", "w", encoding="utf-8") as f:
        count = 0
        for index, row in df.iterrows():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tweet = generate_tweet(row, selected_indices)
            if tweet is not None:
                count += 1

                # Save tweet
                f.write(f"{tweet}\n\n\n")

                # Save image
                image_path = f"Britain/images/tweet_{count}.png"
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
