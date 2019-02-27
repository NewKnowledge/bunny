communities_sql = """
    SELECT DISTINCT cp.community_name
    FROM communities_posts cp
    GROUP BY cp.community_name
"""

url_hops_sql = """
SELECT
    p.post_id,
    p.published_at,
    l.url,
    plat.platform_name
FROM social.platforms plat
JOIN social.posts p ON plat.platform_id = p.platform_id
JOIN social.posts_lINks pl ON pl.post_id = p.post_id
JOIN social.links l ON pl.link_id = l.link_id
JOIN social.communities_posts cp ON cp.post_id = p.post_id
WHERE
    p.published_at >= ? AND
    p.published_at < ? AND
    l.url IS NOT NULL AND
    cp.community_name = ? AND
    l.type='link'
"""