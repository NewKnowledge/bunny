communities_sql = """
    SELECT DISTINCT cp.community_name
    FROM communities_posts cp
    GROUP BY cp.community_name
"""

url_hops_sql = """
    WITH old_links AS (
       SELECT
        DISTINCT l.url AS url,
        plat.platform_name
      FROM social.platforms plat
      JOIN social.posts p ON plat.platform_id = p.platform_id
      JOIN social.posts_lINks pl ON pl.post_id = p.post_id
      JOIN social.links l ON pl.link_id = l.link_id
      JOIN social.communities_posts cp ON cp.post_id = p.post_id
      WHERE
          p.published_at >= %s AND 
          p.published_at < %s AND
          l.url IS NOT NULL AND
          cp.community_name = %s AND
          l.type='link'
    ), new_links AS (
      SELECT
        DISTINCT l.url AS url,
        plat.platform_name
      FROM social.platforms plat
      JOIN social.posts p ON plat.platform_id = p.platform_id
      JOIN social.posts_lINks pl ON pl.post_id = p.post_id
      JOIN social.links l ON pl.link_id = l.link_id
      JOIN social.communities_posts cp ON cp.post_id = p.post_id
      WHERE
          p.published_at >= %s AND
          p.published_at < %s AND
          l.url IS NOT NULL AND
          cp.community_name = %s AND
          l.type='link'
    )
    SELECT nl.url,
           ol.url,
           nl.platform_name,
           ol.platform_name
    FROM new_links nl
      LEFT JOIN old_links ol ON nl.url = ol.url AND nl.platform_name = ol.platform_name
    WHERE nl.url IN
      (
        SELECT DISTINCT url
        FROM old_links
      ) AND
      ol.platform_name IS NULL
"""