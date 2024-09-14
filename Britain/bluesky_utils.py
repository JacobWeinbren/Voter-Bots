import os
from atproto import Client
from datetime import datetime, timezone


def post_to_bluesky(tweet, image_path):
    client = Client()
    client.login(
        os.environ["BRITAIN_BLUESKY_HANDLE"], os.environ["BRITAIN_BLUESKY_PASSWORD"]
    )

    with open(image_path, "rb") as f:
        img_data = f.read()

    # Upload the image first
    upload = client.com.atproto.repo.upload_blob(img_data)

    # Get the current time with timezone information
    created_at = datetime.now(timezone.utc).isoformat()

    # Create the post with the uploaded image
    data = {
        "repo": client.me.did,
        "collection": "app.bsky.feed.post",
        "record": {
            "text": "",
            "embed": {
                "$type": "app.bsky.embed.images",
                "images": [{"alt": tweet, "image": upload.blob}],
            },
            "createdAt": created_at,
        },
    }

    client.com.atproto.repo.create_record(data=data)
