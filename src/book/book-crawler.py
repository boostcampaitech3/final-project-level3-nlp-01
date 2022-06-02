import pstats
from time import sleep
from selenium import webdriver
import pandas as pd

class BookIntroCrawler:
    def __init__(self) -> None:
        pass
    
    def crawl(self):
        data = []
        year = 2022
        month = 5
        book_url = f"http://www.yes24.com/24/category/bestseller?CategoryNumber=001001046&sumgb=09&year={year}&month={month}"

        print('Initialize Drive')
        driver = self.initDrive(book_url)

        print('Start parsing')
        data = self.parse(driver)

        print('data 수:', len(data))

        print('Save to csv')
        data.to_csv(f"Book_top20_{year}_{month}.csv", encoding='utf-8', index=False)

    def initDrive(self, book_url):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정

        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_argument('--disable-dev-shm-usage')

        #### 사용하기 전, 절대경로로 수정해주세요.
        #### 구글 크롬 버전 101.
        driver = webdriver.Chrome('/Users/yejin/Yejin_drive/VSC_projects/final-project-level3-nlp-01/src/chromedriver') # Mac M1
        # driver = webdriver.Chrome('./chromedriver.exe') # Window
        driver.get(book_url)

        return driver

    def parse(self, driver):
        
        Urls = []
        Images = []
        for i in range(1, 61, 2):
            urls = driver.find_elements_by_css_selector(f'#category_layout > tbody > tr:nth-child({i}) > td.goodsTxtInfo > p:nth-child(1) > a:nth-child(1)')
            for j in urls:
                url = j.get_attribute('href')
                Urls.append(url)
            images = driver.find_elements_by_css_selector(f'#category_layout > tbody > tr:nth-child({i}) > td.image > div > a:nth-child(1) > img')
            for k in images:
                image = k.get_attribute('src')
                Images.append(image)
        
        Titles = []
        Authors = []
        Introductions = []
                
        for i in Urls:
            driver.get(i)
            title = driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2')
            Titles.append(title.text)
            author = driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth > a')
            Authors.append(author.text)
            try:
                introduction = driver.find_element_by_css_selector('#infoset_introduce > div.infoSetCont_wrap > table > tbody > tr > td > div > div')
                Introductions.append(introduction.text)
            except:
                introduction = driver.find_element_by_css_selector('#infoset_introduce > div.infoSetCont_wrap > div.infoWrap_txt > div')
                Introductions.append(introduction.text)
            
            
        data = pd.DataFrame({"title":Titles, "author":Authors, "introduction":Introductions, "url":Urls, "image":Images})

        return data

if __name__ == '__main__':
    mc = BookIntroCrawler()
    mc.crawl()