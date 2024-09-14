import os
from atproto import Client


def post_to_bluesky(tweet, image_path):
    client = Client()
    client.login(os.environ["BLUESKY_HANDLE"], os.environ["BLUESKY_PASSWORD"])

    with open(image_path, "rb") as f:
        img_data = f.read()

    # Upload the image first
    upload = client.com.atproto.repo.upload_blob(img_data)

    # Create the post with the uploaded image
    client.com.atproto.repo.create_record(
        repo=client.me.did,
        collection="app.bsky.feed.post",
        record={
            "text": "",
            "embed": {
                "$type": "app.bsky.embed.images",
                "images": [{"alt": tweet, "image": upload.blob}],
            },
        },
    )
