import json
import re

import requests
from konlpy.tag import Okt

from db.db_service import DBService
from db.query_mapper import QueryMapper
from model.condition_type import ConditionType
from project.config import Config


def collect_from_wanted(start_url):

    detail_urls = _get_detail_urls(start_url)
    print('detail_url_count', len(detail_urls))

    recruit_notices = get_nouns_from_detail_url(detail_urls)

    # print(requirements_nouns)
    # print(preferred_points_nouns)

    store_to_db(recruit_notices)


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

    recruit_notices = []

    for detail_url in detail_urls:
        resp = requests.get(detail_url)
        resp_body = json.loads(resp.text)
        print("resp body : ", resp_body)

        company = resp_body['job']['company']['name']
        detail = resp_body['job']['detail']
        requirements = detail['requirements']
        preferred_points = detail['preferred_points']

        requirements_nouns = extract_english_nouns(requirements)
        requirements_nouns += extract_korean_nouns(requirements)

        preferred_points_nouns = extract_english_nouns(preferred_points)
        preferred_points_nouns += extract_korean_nouns(preferred_points)

        recruit_notices.append({'company': company,
                                'condition_type': ConditionType.REQUIRED,
                                "keywords": requirements_nouns})

        recruit_notices.append({'company': company,
                                'condition_type': ConditionType.PREFERRED,
                                "keywords": preferred_points_nouns})

    return recruit_notices


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
    nouns = re.findall(r'[a-zA-Z\-]{2,}', text)
    uppercase_nouns = [noun.upper() for noun in nouns]
    return uppercase_nouns


def store_to_db(recruit_notices):
    db_service = DBService(host=Config.get('db.url')
                          , user=Config.get('db.username')
                          , password=Config.get('db.password')
                          , db=Config.get('db.name')
                          , charset='utf8')

    cursor = db_service.get_cursor();

    for recruit_notice in recruit_notices:

        # print(recruit_notice['company'], str(recruit_notice['condition_type']))

        query = QueryMapper.insert_raw_collection()
        cursor.execute(query, (recruit_notice['company']
                               , recruit_notice['condition_type'].value)
                       )

        raw_collection_id = db_service.get_last_id()

        keywords = recruit_notice['keywords']
        for keyword in keywords:
            query = QueryMapper.insert_raw_word()
            cursor.execute(query, (keyword, raw_collection_id))

    db_service.commit_and_close()
