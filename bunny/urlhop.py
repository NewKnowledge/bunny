import json


class URLHop(object):

    unique_instances = {}

    def __new__(cls, community, new_url_row, matches):
        url = new_url_row['url']
        platform = new_url_row['platform_name']
        try:
            return cls.unique_instances[(community, url, platform)]
        except KeyError:
            return super(URLHop, cls).__new__(cls)


    def __init__(self, community, new_url_row, matches):
        self.community = community
        self.platform = new_url_row['platform_name']
        self.url = new_url_row['url']
        self.post_id = int(new_url_row['post_id'])
        self.published_at = str(new_url_row['published_at'])
        self._old_posts_df = matches
        self.old_posts = []
        self._create_old_platform_posts()
        URLHop.unique_instances[(community, self.url, self.platform)] = self


    def _create_old_platform_posts(self):
        for platform in self._old_posts_df['platform_name'].unique():
            posts_for_platform = self._old_posts_df[self._old_posts_df['platform_name'] == platform]
            newest_post = posts_for_platform.sort_values(by='published_at', ascending=False).iloc[0]
            self.old_posts.append({'platform': platform,
                                   'post_id': int(newest_post['post_id']),
                                   'published_at': str(newest_post['published_at'])})


    def create_json(self):
        json_dict = {'url': self.url,
                     'version': 'v1',
                     'community': self.community,
                     'new_post': {'platform': self.platform,
                                  'post_id': self.post_id,
                                  'published_at': self.published_at},
                     'old_posts': self.old_posts}

        return json.dumps(json_dict)