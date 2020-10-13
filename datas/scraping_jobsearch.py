from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import datetime

def scrapping_worknet(max_page=10, keyword='AI'):
    # 드라이버 옵션
    options = webdriver.ChromeOptions()
    options.add_argument('headless')    # headless mode
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # 드라이버 연결
    driver = webdriver.Chrome(executable_path='./datas/chromedriver', chrome_options=options)
    driver.get(url='https://www.work.go.kr')
    print('start chrome driver')

    # 검색 및 더보기
    search_box = driver.find_element(By.NAME, 'topQuery')
    search_box.send_keys(keyword)
    print(f'keyword: {keyword}')
    driver.find_element(By.CLASS_NAME, 'btn-search').click()
    btn1 = driver.find_elements(By.XPATH, '//*[@id="contents"]/div/div[1]/div[1]/div[2]/div[3]/a')
    btn1[0].click()
    print(f'more click')

    # 몽고디비 연결
    with MongoClient('mongodb://127.0.0.1:27017/')  as client:
        mydb = client.mydb
        print('MongoDB connect')
        page = 1
        while True:
            for page_num in range(3,13):    # page a tag number
                titles = driver.find_elements_by_class_name('link') 
                companies = driver.find_elements_by_class_name('txt')
                data = []
                for title, company in zip(titles, companies[2:12]):
                    href = title.find_element(By.TAG_NAME,'a').get_attribute('href')
                    data.append({'title': title.text, 'company':company.text, 'link':href, "create_date": datetime.datetime.now()}) 
                mydb.worknet.insert_many(data)
                print(f'{page} page completion')

                # 종료 조건
                if page==max_page:
                    print('system exit')
                    driver.quit()
                    return
                else:
                    page = page + 1
                    driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div[1]/div[1]/nav/a[{page_num}]').click()

def scrapping_jobkorea(max_page=10, keyword='AI'):
    for page in range(max_page):
        res = requests.get(f'http://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit&Page_No={str(page)}')
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            links = soup.find_all('a', class_='title dev_view')
            companies = soup.find_all('a', class_='name dev_view')
            data = []
            for link, company in zip(links, companies):
                title = link.get_text()
                link = 'http://www.jobkorea.co.kr' + link.get('href')
                company_name = company.get_text()
                dic = {"title": title, "link": link, "company":company_name, "create_date": datetime.datetime.now()}
                data.append(dic)

            with MongoClient('mongodb://127.0.0.1:27017/')  as client:
                mydb = client.mydb
                res = mydb.jobkorea.insert_many(data)

if __name__ == "__main__":
    scrapping_jobkorea()
    scrapping_worknet()