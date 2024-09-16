from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def generate_chat_bubble(tweet):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        tweet_html = tweet.replace("\n", "<br>")

        html_content = f"""
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Nunito', sans-serif; }}
                .bubble-arrow::before {{
                    content: '';
                    position: absolute;
                    bottom: -20px;
                    left: 20px;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-top: 20px solid #fff;
                    filter: drop-shadow(0 4px 3px rgb(0 0 0 / 0.07));
                }}
            </style>
        </head>
        <body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
            <div class="max-w-2xl w-full bg-white rounded-2xl shadow-lg p-6 relative bubble-arrow">
                <p class="text-gray-800 text-lg leading-relaxed">{tweet_html}</p>
            </div>
        </body>
        </html>
        """

        try:
            page.set_content(html_content, timeout=60000)
        except PlaywrightTimeoutError:
            print(f"Timeout occurred while setting content for tweet: {tweet[:50]}...")
            browser.close()
            return None

        content_box = page.query_selector("body > div").bounding_box()
        page.set_viewport_size(
            {
                "width": int(content_box["width"]) + 40,
                "height": int(content_box["height"]) + 40,
            }
        )

        screenshot = page.screenshot(full_page=True)
        browser.close()

    return screenshot


def save_chat_bubble_image(tweet, output_path):
    screenshot = generate_chat_bubble(tweet)
    if screenshot:
        with open(output_path, "wb") as f:
            f.write(screenshot)
        return True
    return False
