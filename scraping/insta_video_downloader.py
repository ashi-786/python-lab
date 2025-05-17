import os
from dotenv import load_dotenv
import instaloader
from urllib.parse import urlparse

# Load credentials from .env
load_dotenv()
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

L = instaloader.Instaloader(
    download_comments=False,
    save_metadata=False,
    post_metadata_txt_pattern='',
    filename_pattern='{shortcode}',
    download_geotags=False,
    download_video_thumbnails=False,
    compress_json=False,
)

# Optional: login for private/restricted content
# L.login(username, password)

post_url = 'https://www.instagram.com/reel/DAeGqNYOgFF/?igsh=cWx0eHg4NXVuY2hi'
# shortcode = post_url.strip('/').split('/')[-1]

path = urlparse(post_url).path  # e.g., "/reel/DAeGqNYOgFF/"
parts = [p for p in path.strip('/').split('/') if p]
if 'reel' in parts and len(parts) > 1:
    shortcode = parts[1]

post = instaloader.Post.from_shortcode(L.context, shortcode)
L.download_post(post, target='media')
