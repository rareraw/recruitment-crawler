import requests
import json

class WantedCrawler():
    def __init__(self):
        pass

    def _get_detail_urls(self):
        resp = requests.get(
            'https://www.wanted.co.kr/api/v4/jobs?1555150187100&country=kr&tag_type_id=518&job_sort=job.latest_order&years=-1&employee_count=all&locations=all')
        resp_body = json.loads(resp.text)
        announcements = resp_body['data']

        urls = []
        for announcement in announcements:
            # url = 'https://www.wanted.co.kr/wd/' + str(announcement['id']) + '?referer_id = 265260'
            url = 'https://www.wanted.co.kr/api/v4/jobs/' + str(announcement['id']) + '?1555153291849'
            urls.append(url)

        return urls

    # def _parse(self):
        