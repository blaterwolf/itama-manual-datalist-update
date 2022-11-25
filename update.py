from facebook_scraper import *
import pandas as pd
import os
import time

results = []
start_url = 'https://m.facebook.com/page_content_list_view/more/?page_id=1624618274297104&start_cursor={"timeline_cursor":"AQHRzAhMDIapJ3JmBVUow7QviDy7lsh3stVV8jy-zwakk0MyhMS4BIv8e0JuZjo70mvlZzIwynB6SwbkeCdBxYqPTENmIEmEKPKUeui-AWwetG34RyMtR-rwZXJfuOMQrrOo","timeline_section_cursor":null,"has_next_page":true}&num_to_fetch=200&surface_type=posts_tab'
start = time.time()


def handle_pagination_url(url):
    global start_url
    start_url = url


set_cookies("cookies.txt")
while True:
    try:
        for post in get_posts("FactCheckPhils", page_limit=None, start_url=start_url, request_url_callback=handle_pagination_url):
            os.system("cls")
            # * data needed
            data_needed = {
                'fb_link': post['post_url'],
                'text': post['text'],
                'post_date': str(post['time']),
                'image_link': post['image_lowquality'],
                'tags': '',
                'fb_link_id': post['post_id'],
            }
            # * for printing
            parsed = json.dumps(data_needed, indent=4,
                                sort_keys=True)  # >> for printing
            print(parsed, "\n")

            # * append to list
            results.append(data_needed)
            # * number of posts retrieved and time taken
            print(
                f"{len(results)} retrieved in {round(time.time() - start)}s.")
        print("ALL DONE. Saving to csv.")
        dataset = pd.DataFrame.from_records(results)
        dataset.to_csv(f'1002_onwards_dataset{len(results)}.csv', index=False)
        print("Saved to csv.")
        break
    except exceptions.TemporarilyBanned:
        print("Temporarily banned, sleeping for 10m")
        time.sleep(600)
        continue
