import os
import random
import shutil


def randomize_tweets():
    # Read all tweets
    with open("Britain/tweets/tweets.txt", "r", encoding="utf-8") as f:
        tweets = f.read().split("\n\n\n")

    # Remove the first tweets
    tweets = tweets[20:]

    # Create a list of tuples (tweet, original_index)
    indexed_tweets = list(enumerate(tweets, start=1))

    # Randomize the list
    random.shuffle(indexed_tweets)

    # Create random_images folder if it doesn't exist
    if not os.path.exists("Britain/random_images"):
        os.makedirs("Britain/random_images")

    # Write the randomized tweets and move corresponding images
    with open("Britain/tweets/random_tweets.txt", "w", encoding="utf-8") as f:
        for new_index, (original_index, tweet) in enumerate(indexed_tweets):
            f.write(tweet + "\n\n\n")

            old_image_path = f"Britain/images/tweet_{original_index}.png"
            new_image_path = f"Britain/random_images/tweet_{new_index}.png"
            if os.path.exists(old_image_path):
                shutil.copy(old_image_path, new_image_path)

    print("Tweets randomized and saved to random_tweets.txt")
    print("Corresponding images copied to random_images folder")


if __name__ == "__main__":
    randomize_tweets()
