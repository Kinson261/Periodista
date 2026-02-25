import dotenv
from flask import Flask, send_file
from playwright.sync_api import sync_playwright
import io
import os

app = Flask(__name__)

URL = os.getenv("BROWSERLESS_URL")
TOKEN = os.getenv("BROWSERLESS_TOKEN")

@app.route("/image", methods=["GET"])
def capture_image():
    try:
        with sync_playwright() as p:
            # browser = p.chromium.connect(
            browser = p.chromium.connect_over_cdp(
                "{}?token={}".format(URL, TOKEN))
            try:
                context = browser.new_context()
                page = context.new_page()

                page.goto("https://www.reddit.com")
                page.wait_for_timeout(5000)
                screenshot = page.screenshot(type="png")

                return send_file(io.BytesIO(screenshot), mimetype="image/png")
            finally:
                browser.close()
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return "Error capturing screenshot", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
    capture_image()
