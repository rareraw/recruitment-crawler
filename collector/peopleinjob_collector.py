import requests
from bs4 import BeautifulSoup
import re

#피플인잡 메인 도메인
main_domain = 'https://www.peoplenjob.com/'

#메인 화면에서 IT관련된 카테고리 뽑기
def get_IT_div(html_datas, key_word) :
    print("Function get_IT_div Start..............")
    for html_data in html_datas :
        html_data_div = html_data.find('div', {'class' : 'panel-heading'})
        if html_data_div.find('a').text == key_word :
            print("Function get_IT_div End..............")
            return html_data

#IT관련된 카테고리 URL 리스트로 뽑기
def get_detail_url_list(url) :
    print("Function get_detail_url_list Start..............")

    detail_url = []

    response = requests.get(url + 'jobs/work')
    raw_html_data = BeautifulSoup(response.text, 'html.parser')

    temp_html_data1 = raw_html_data.findAll('div', {'class': 'panel'})

    temp_html_data2_1 = get_IT_div(temp_html_data1, '인터넷')
    temp_html_data2_2 = get_IT_div(temp_html_data1, '정보통신,전자,전산')

    temp_html_data3_1 = temp_html_data2_1.select('li > a')
    temp_html_data3_2 = temp_html_data2_2.select('li > a')

    for temp_data4 in temp_html_data3_1 :
        detail_url.append(temp_data4.get('href'))

    for temp_data4 in temp_html_data3_2 :
        detail_url.append(temp_data4.get('href'))

    print("Function get_detail_url_list End..............")
    return detail_url


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
            raw_html_data = BeautifulSoup(response.text, 'html.parser')

            temp_html_data1 = raw_html_data.findAll('td',{'class':'job-title'})

            for temp_html_data2 in temp_html_data1 :
                temp_html_data3 = temp_html_data2.find('a').get('href')
                detail_detail_url_list.append(temp_html_data3)

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

    print(get_detail_page_url_list)

    print("Function get_detail_page_url End..............")

detail_url_list = get_detail_url_list(main_domain)
start_crawling(main_domain, detail_url_list)
#get_detail_page_url(["https://www.peoplenjob.com//jobs?type=work&work_code_id=146&page=1","https://www.peoplenjob.com//jobs?type=work&work_code_id=146&page=2"])