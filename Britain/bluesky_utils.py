import os
from atproto import Client


def post_to_bluesky(tweet, image_path):
    client = Client()
    client.login(os.environ["BRITAIN_BLUESKY_HANDLE"], os.environ["BLUESKY_PASSWORD"])

    with open(image_path, "rb") as f:
        img_data = f.read()

    client.post(text="", image=img_data, image_alt=tweet)
