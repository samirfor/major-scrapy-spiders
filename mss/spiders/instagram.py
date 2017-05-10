import re
import json

from scrapy import Spider, Item, Field

class InstagramProfileItems(Item):
    is_private = Field()
    posts = Field()
    username = Field()
    biography = Field()
    website = Field()
    profile_picture = Field()
    full_name = Field()
    total_posts = Field()
    followers = Field()
    following = Field()

class Instagram(Spider):
    name = 'Instagram'
    start_urls = [
        'https://instagram.com/nike/',
    ]

    download_delay = 0.5

    def parse(self, response):
        javascript = ''.join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        json_data = json.loads(''.join(re.findall(r'window._sharedData = (.*);', javascript)))

        item = InstagramProfileItems()
        data = json_data['entry_data']['ProfilePage'][0]['user']
        item['is_private'] = data['is_private']
        item['posts'] = data['media']['nodes']
        item['username'] = data['username']
        item['biography'] = data['biography']
        item['website'] = data['external_url']
        item['profile_picture'] = data['profile_pic_url_hd']
        item['full_name'] = data['full_name']
        item['total_posts'] = data['media']['count']
        item['followers'] = data['followed_by']['count']
        item['following'] = data['follows']['count']
        return item
