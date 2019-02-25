from datetime import datetime, timedelta, timezone
import pandas as pd
from bunny import app
from bunny.config import SNOWFLAKE_CONFIG, OLD_WINDOW_BEGINNING, OLD_WINDOW_END, NEW_WINDOW_BEGINNING, NEW_WINDOW_END, PIVOT_TIME
from bunny.workers.sql import communities_sql, url_hops_sql
from nk_snowflake.base import query_all


def retrieve_all_communities(config):
    return [row[0] for row in query_all(config, communities_sql)]


class URLHop(object):

    unique_dict = {}

    def __new__(cls, community, url, _from, to):
        try:
            cls.unique_dict[(community, url, _from, to)]
            return None
        except KeyError:
            return super(URLHop, cls).__new__(cls)

    def __init__(self, community, url, _from, to):
        URLHop.unique_dict[(community, furl, _from, to)] = None



def find_url_hops_for_community(config, community):
    #DEBUG
    PIVOT_TIME = datetime(year=2018, month=10, day=15, hour=2, minute=0, second=0, tzinfo=timezone.utc)
    OLD_WINDOW_BEGINNING = PIVOT_TIME - timedelta(days=30)
    NEW_WINDOW_END = PIVOT_TIME + timedelta(hours=1)

    old_url_params = (
        ("TIMESTAMP_TZ", OLD_WINDOW_BEGINNING),
        ("TIMESTAMP_TZ", NEW_WINDOW_END),
        community)

    all_posts = query_all(config, url_hops_sql, qparams=old_url_params)
    print("received data")
    posts_df = pd.DataFrame(all_posts, columns=['post_id', 'published_at', 'url', 'platform_name'])
    posts_df['before_pivot'] = posts_df['published_at'].apply(lambda x: True if x < PIVOT_TIME else False).astype(bool)

    print("Iterating rows")
    url_hops = []
    for idx,row in posts_df.loc[posts_df['before_pivot'] == False].iterrows():
        matching_urls = posts_df[(posts_df['before_pivot'] == True) &
                                 (posts_df['url'] == row['url']) &
                                 (posts_df['platform_name'] != row['platform_name'])]
        #TODO: Create a new URLHop per platform!
        if len(matching_urls) > 0:
            hop = URLHop(community, url)
        pass

    return all_posts



if __name__ == "__main__":
    #communities = retrieve_all_communities(SNOWFLAKE_CONFIG)
    communities=['tesla']
    for community in communities:
        print("Working %s" % community)
        urls = find_url_hops_for_community(SNOWFLAKE_CONFIG, community)