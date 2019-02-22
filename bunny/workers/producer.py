from bunny import app
from bunny.config import SNOWFLAKE_CONFIG, OLD_WINDOW_BEGINNING, OLD_WINDOW_END, NEW_WINDOW_BEGINNING, NEW_WINDOW_END
from bunny.workers.sql import communities_sql, url_hops_sql
from nk_snowflake.base import query_all


def retrieve_all_communities(config):
    return [row[0] for row in query_all(config, communities_sql)]


def find_url_hops_for_community(config, community):
    params = (
        ("TIMESTAMP_TZ", OLD_WINDOW_BEGINNING),
        ("TIMESTAMP_TZ", OLD_WINDOW_END),
        community,
        ("TIMESTAMP_TZ", NEW_WINDOW_BEGINNING),
        ("TIMESTAMP_TZ", NEW_WINDOW_END),
        community
    )
    results = query_all(config, url_hops_sql, qparams=params)

    return results



if __name__ == "__main__":
    communities = retrieve_all_communities(SNOWFLAKE_CONFIG)
    for community in communities:
        print("Working %s" % community)
        urls = find_url_hops_for_community(SNOWFLAKE_CONFIG, community)