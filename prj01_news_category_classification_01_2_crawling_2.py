from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
import time
import pandas as pd
import re

options = webdriver.ChromeOptions()
#options.add_argument('headless') # 브라우저 안보이기
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
options.add_argument('lang=ko')
driver = webdriver.Chrome('../chromedriver', options=options)
driver.implicitly_wait(10)

#빈 데이터프레임
df_title = pd.DataFrame()
df_section_title = pd.DataFrame()

title_list = [] #빈 리스트 생성
for k in range(301, 423):
    url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page={}'.format(k)
    driver.get(url)
    time.sleep(0.7)
    for j in range(1, 5): #X path로 확인한 ul 요소 1~4
        for i in range(1, 6): #X path 확인한 li 요소 1~5
            try:
                title = driver.find_element_by_xpath(
                    '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[last()]/a'.format(j, i)
                ).text
                title = (re.compile('[^가-힣|a-z|A-Z]').sub(' ', title)) # 정규표현식 전처리
                print(title)
                title_list.append(title)
            except NoSuchFrameException: # 엘리먼스 리스 오류
                print('NoSuchElementException')

df_section_title = pd.DataFrame(title_list, columns=['title'])
df_section_title['category'] = 'Economic'
df_title = pd.concat([df_title, df_section_title], axis=0, ignore_index=True)

driver.close()
df_title.head(30)

df_title.to_csv(f'./crawling_data/naver_news_titles_301-422_{time.strftime("%Y-%m-%d", time.localtime(time.time()))}.csv', index=False)