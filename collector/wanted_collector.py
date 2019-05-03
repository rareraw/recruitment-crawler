import json
import re

import requests
from konlpy.tag import Okt


def collect_from_wanted(start_url):

    detail_urls = _get_detail_urls(start_url)
    print('detail_url_count', len(detail_urls))

    requirements_nouns, preferred_points_nouns = get_nouns_from_detail_url(detail_urls)

    print(requirements_nouns)
    print(preferred_points_nouns)

    save_to_db(requirements_nouns, preferred_points_nouns)


def _get_detail_urls(start_url):
    resp = requests.get(start_url)
    resp_body = json.loads(resp.text)
    announcements = resp_body['data']

    detail_urls = []
    for announcement in announcements:
        url = 'https://www.wanted.co.kr/api/v4/jobs/' + str(announcement['id']) + '?1555153291849'
        detail_urls.append(url)

    return detail_urls


def get_nouns_from_detail_url(detail_urls):

    requirements = ''
    preferred_points = ''

    for detail_url in detail_urls:
        resp = requests.get(detail_url)
        resp_body = json.loads(resp.text)
        detail = resp_body['job']['detail']
        requirements += detail['requirements']
        preferred_points += detail['preferred_points']

    requirements_nouns = extract_english_nouns(requirements)
    preferred_points_nouns = extract_english_nouns(preferred_points)

    requirements_nouns += extract_korean_nouns(requirements)
    preferred_points_nouns += extract_korean_nouns(preferred_points)

    # print(requirements, preferred_points)
    return requirements_nouns, preferred_points_nouns


def extract_korean_nouns(text):

    except_nouns = ['개발', '경험', '실무', '사용', '기반', '이상', '구축', '자유', '자재', '활용',
                    '지식', '역량', '통신', '프로젝트', '성향', '가능', '서비스', '배포', '관리',
                    '경력', '습듭', '열정', '지속', '대해', '연구', '관심', '코드', '개발자',
                    '최소', '마음', '적극', '이해', '통한', '고집', '프로세스', '능력', '대한',
                    '보유', '기본', '관련', '학과', '졸업', '여러', '중시', '수평', '멤버',
                    '어려움', '위해', '노력', '학습', '나은', '주도', '이용', '특허', '흥미',
                    '도구', '산업', '고민', '환경', '스펙', '등록', '의견', '환경', '근무',
                    '무관', '언어', '자신', '매우', '과제', '시장', '확신', '논리', '분석',
                    '학력', '연차', '문법', '숙련']

    nouns = Okt().nouns(text)
    filtered_nouns = []
    for noun in nouns:
        if len(noun) > 1 and noun not in except_nouns:
            filtered_nouns.append(noun)
    return filtered_nouns


def extract_english_nouns(text):
    return re.findall(r'[a-zA-Z\-]{2,}', text)


def save_to_db(requirements_nouns, preferred_points_nouns):
    pass


if __name__ == '__main__':
    collect_from_wanted('https://www.wanted.co.kr/api/v4/jobs?1555240925294&country=kr&tag_type_id=518&job_sort=job.popularity_order&years=-1&employee_count=all&locations=all')
