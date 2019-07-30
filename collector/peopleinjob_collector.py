import re

import requests

from bs4 import BeautifulSoup
from konlpy.tag import Okt

from db.db_service import DBService
from project.config import Config
from model.condition_type import ConditionType
from db.query_mapper import QueryMapper



#피플인잡 메인 도메인, SEQ 가져오기
#Input : 서비스명
#Output : 서비스 Seq, 서비스 main domain
def _get_peopleinjob_info(service_name) :
    db_service = DBService(host=Config.get('db.url')
                           , user=Config.get('db.username')
                           , password=Config.get('db.password')
                           , db=Config.get('db.name')
                           , charset='utf8')

    return db_service.select_one(QueryMapper.select_recruitment_site_query, service_name)

#해당 카테고리에서 분류 URL 리스트로 뽑기
#Input : 메인도메인, 카테고리명
#Output : 분류리스트
def _get_detail_url_list(main_domain, category_name) :
    detail_url = []
    print("Function get_detail_url_list Start..............")

    response = requests.get(main_domain + '/jobs/work')
    raw_html_data = BeautifulSoup(response.text, 'html.parser')

    html_category_list = raw_html_data.findAll('div', {'class': 'panel'})

    #html_category_data = get_IT_div(html_category_list, category_name)
    html_category_data = ""
    for html_category in html_category_list :
        html_data_div = html_category.find('div', {'class' : 'panel-heading'})
        if html_data_div.find('a').text == category_name :
            html_category_data = html_data_div

    temp_html_data3_2 = html_category_data.select('li > a')
    print(temp_html_data3_2)

    for temp_data4 in temp_html_data3_2 :
        detail_url.append(temp_data4.get('href'))

    print("Function get_detail_url_list End..............")
    return detail_url

main_domain = _get_peopleinjob_info('PeopleInJob')
_get_detail_url_list(main_domain,'정보통신,전자,전산')




#main_domin : 컨텍스트루트, detail_list : IT->웹개발자,앱개발자,퍼블리셔 등등 소분류 카테고리 접근 URL
def start_crawling(main_domain, detail_url_list) :
    print("Function start_crawling Start..............")

    #상세 공고페이지 URL 담아낼 리스트
    detail_detail_url_list = []

    for detail_url in detail_url_list :

        page_count = 1

        #다음 페이지라는 버튼이 비화성화 될때까지 루프
        while True:
            print("requesting url >>>>>> " + main_domain + detail_url + '&page=' + str(page_count))
            response = requests.get(main_domain + detail_url + '&page=' + str(page_count))
            detail_detail_url_list.append(main_domain + detail_url + '&page=' + str(page_count))
            raw_html_data = BeautifulSoup(response.text, 'html.parser')

            if not raw_html_data.find('ul',{'class':'pagination'}) :
                print("There isn't another page..... moving to next category")
                break

            last_page_check = raw_html_data.find('ul',{'class':'pagination'}).findAll('li')
            if last_page_check[len(last_page_check) - 1].find('a') :
                page_count += 1
            elif page_count > 100 : #무한루프 풀기위한 방어코드
                print('something went wrong')
                break
            else :
                print('Reached last page count >>> ' + str(page_count) + "..... moving to next category")
                break

    print(detail_detail_url_list)
    print("Function start_crawling End..............")

    return detail_detail_url_list

#상세페이지 URL 가져오기
def get_detail_page_url(detail_detail_url_list) :
    print("Function get_detail_page_url Start..............")

    get_detail_page_url_list = []

    for detail_detail_url in detail_detail_url_list :
        response = requests.get(detail_detail_url)
        raw_html_data = BeautifulSoup(response.text, 'html.parser')
        temp_html_data1 = raw_html_data.find('table', {'class': 'table-job-list'}).findAll('td', {'class': 'job-title'})

        for temp_html_data2 in temp_html_data1 :
            temp_html_data3 = temp_html_data2.find('a').get('href')

            #광고성 목록 지우기
            if main_domain in  temp_html_data3:
                get_detail_page_url_list.append(temp_html_data3)

    print("Function get_detail_page_url End..............")

    return get_detail_page_url_list

#상세페이지에서 데이터 가져오기
def get_detail_raw_text(get_detail_page_url_list):
        for get_detail_page_url in get_detail_page_url_list:
            response = requests.get(get_detail_page_url)
            raw_html_data = BeautifulSoup(response.text, 'html.parser')
            temp_html_data1 = raw_html_data.find('div', {'class': 'divDetailWrap'})
            nouns = Okt().nouns(temp_html_data1.text)
            eng_nouns = re.findall(r'[a-zA-Z\-]{2,}', temp_html_data1.text)
            print(nouns+eng_nouns)

#detail_url = get_detail_url_list(main_domain)
#detail_detail_url_list = start_crawling(main_domain, detail_url)
#get_detail_page_url_list = get_detail_page_url(['https://www.peoplenjob.com/jobs?type=work&work_code_id=137&page=1'])
#get_detail_raw_text(get_detail_page_url_list)
