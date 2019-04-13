import requests
import json


class WantedCrawler():
    def __init__(self):
        self.detail_urls = []
        self._init_detail_urls()

    def _init_detail_urls(self):
        resp = requests.get(
            'https://www.wanted.co.kr/api/v4/jobs?1555150187100&country=kr&tag_type_id=518&job_sort=job.latest_order&years=-1&employee_count=all&locations=all')
        resp_body = json.loads(resp.text)
        announcements = resp_body['data']

        for announcement in announcements:
            # url = 'https://www.wanted.co.kr/wd/' + str(announcement['id']) + '?referer_id = 265260'
            url = 'https://www.wanted.co.kr/api/v4/jobs/' + str(announcement['id']) + '?1555153291849'
            self.detail_urls.append(url)

    def parse(self):
        # print(self.detail_urls)
        for detail_url in self.detail_urls:
            requests.get(detail_url)


