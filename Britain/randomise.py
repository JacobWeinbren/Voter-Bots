import os
import random
import shutil


def reorganize_tweets():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct absolute paths
    tweets_dir = os.path.join(script_dir, "tweets")
    original_tweets_file = os.path.join(tweets_dir, "tweets.txt")
    random_tweets_file = os.path.join(tweets_dir, "random_tweets.txt")
    original_images_dir = os.path.join(script_dir, "images")
    random_images_dir = os.path.join(script_dir, "random_images")

    # Create directories if they don't exist
    os.makedirs(tweets_dir, exist_ok=True)
    os.makedirs(random_images_dir, exist_ok=True)

    # Check if the original tweets file exists
    if not os.path.exists(original_tweets_file):
        print(f"Error: {original_tweets_file} does not exist.")
        return

    # Read all tweets from the original file
    with open(original_tweets_file, "r", encoding="utf-8") as f:
        tweets = f.read().split("\n\n\n")

    # Remove empty tweets
    tweets = [tweet.strip() for tweet in tweets if tweet.strip()]

    # Ensure we have at least 20 tweets
    if len(tweets) < 20:
        print(
            f"Error: Not enough tweets in {original_tweets_file}. Found {len(tweets)}, need at least 20."
        )
        return

    # Remove the first 20 tweets
    tweets = tweets[20:]

    # Create a list of tuples (tweet, original_index)
    indexed_tweets = list(enumerate(tweets, start=20))

    # Randomize the order of remaining tweets
    random.shuffle(indexed_tweets)

    # Write the randomized tweets to the random_tweets.txt file
    with open(random_tweets_file, "w", encoding="utf-8") as f:
        for new_index, (original_index, tweet) in enumerate(indexed_tweets):
            f.write(f"{tweet}\n\n\n")

            # Copy and rename the corresponding image if it exists
            original_image_path = os.path.join(
                original_images_dir, f"tweet_{original_index}.png"
            )
            new_image_path = os.path.join(random_images_dir, f"tweet_{new_index}.png")
            if os.path.exists(original_image_path):
                shutil.copy2(original_image_path, new_image_path)
                print(
                    f"Copied and renamed tweet_{original_index}.png to tweet_{new_index}.png"
                )
            else:
                print(f"Warning: Image not found for tweet_{original_index}")

    print(f"Reorganized {len(indexed_tweets)} tweets and renamed corresponding images.")


if __name__ == "__main__":
    reorganize_tweets()
