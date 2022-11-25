import time
from facebook_scraper import *

results = []
start_url = None


def handle_pagination_url(url):
    global start_url
    start_url = url
    if results:
        print(f"{len(results)}: {results[-1]['time']}: {start_url}")


set_cookies("cookies.txt")
while True:
    try:
        for post in get_posts("FactCheckPhils", page_limit=None, start_url=start_url, request_url_callback=handle_pagination_url, options={
            "allow_extra_requests": False,
            "posts_per_page": 200
        }):
            results.append(post)
        print("All done")
        break
    except exceptions.TemporarilyBanned:
        print("Temporarily banned, sleeping for 10m")
        time.sleep(600)
