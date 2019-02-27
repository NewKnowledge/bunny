from bunny.config import SNOWFLAKE_CONFIG, FULL_WINDOW_BEGINNING, FULL_WINDOW_END, PIVOT_TIME
from bunny.sql import communities_sql
from bunny.consumer import find_url_hops_for_community
from nk_snowflake.base import query_all


if __name__ == "__main__":

    communities = [row[0] for row in query_all(SNOWFLAKE_CONFIG, communities_sql)]
    # communities=['tesla']
    for community in communities:
        print("Working %s" % community)
        find_url_hops_for_community.apply_async(args=(community, FULL_WINDOW_BEGINNING, FULL_WINDOW_END, PIVOT_TIME))
