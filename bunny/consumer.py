import pandas as pd
from datetime import datetime, timezone
from nk_snowflake import query_all

from bunny.app import app
from bunny.config import SNOWFLAKE_CONFIG, WORKER_PROCESSES
from bunny.sql import url_hops_sql
from bunny.urlhop import URLHop


@app.task
def find_url_hops_for_community(community, window_beginning, window_end, pivot_time):
    # #DEBUG
    # PIVOT_TIME = datetime(year=2018, month=10, day=15, hour=2, minute=0, second=0, tzinfo=timezone.utc)
    # OLD_WINDOW_BEGINNING = PIVOT_TIME - timedelta(days=30)
    # NEW_WINDOW_END = PIVOT_TIME + timedelta(hours=1)
    window_beginning = datetime.strptime(window_beginning, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    window_end = datetime.strptime(window_end, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    pivot_time = datetime.strptime(pivot_time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

    qparams = (
        ("TIMESTAMP_TZ", window_beginning),
        ("TIMESTAMP_TZ", window_end),
        community)

    all_posts = query_all(SNOWFLAKE_CONFIG, url_hops_sql, qparams=qparams)
    print("received data")
    posts_df = pd.DataFrame(all_posts, columns=['post_id', 'published_at', 'url', 'platform_name'])
    posts_df['before_pivot'] = posts_df['published_at'].apply(lambda x: True if x < pivot_time else False).astype(bool)

    print("Finding hops")
    new_urls = posts_df[posts_df['before_pivot'] == False]
    for idx, new_url in new_urls.iterrows():
        old_url_matches = posts_df[(posts_df['before_pivot'] == True) & (posts_df['url'] == new_url['url'])]

        # No old URLs, no hop
        if old_url_matches.empty or not :
            continue
        # URL has already appeared on platform
        elif not old_url_matches[old_url_matches['platform_name'] == new_url['platform_name']].empty:
            continue
        # URL hopped
        else:
            URLHop(community, new_url, old_url_matches)

    print("")


if __name__ == "__main__":
    app.worker_main(argv=['worker','--concurrency=%s' % WORKER_PROCESSES])