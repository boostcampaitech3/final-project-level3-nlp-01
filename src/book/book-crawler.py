import pstats
from time import sleep
from selenium import webdriver
import pandas as pd

class BookIntroCrawler:
    def __init__(self) -> None:
        pass
    
    def crawl(self):
        data = []
        book_url = "https://book.naver.com/bestsell/bestseller_list.naver?type=image&cp=yes24&cate=001001044"

        print('Initialize Drive')
        driver = self.initDrive(book_url)

        print('Start parsing')
        data = self.parse(driver)

        print('data 수:', len(data))

        print('Save to csv')
        data.to_csv(f"Book_top25.csv", encoding='utf-8', index=False)

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
        titles = driver.find_elements_by_class_name('list_1')
        titles2 = []
        for i in titles:
            titles2.append(i.text)

        del titles2[25:]

        author = driver.find_elements_by_class_name('')
        authors = []
        
        

        numbers = []
        songTagList = driver.find_elements_by_css_selector('#lst50 > td:nth-child(4) > div > button.btn_icon.play')
        for i in songTagList:
            num = i.get_attribute('onclick')[31:39]
            if num[-1] == ')':
                num = num.replace(')', '')
            numbers.append(num)
        
        urls = []    
        Introductions = []
        for i in numbers:
            url = "https://book.naver.com/bookdb/book_detail.naver?bid=" + i
            urls.append(url)
            driver.get(url)
            try:
                introduction = driver.find_element_by_class_name('introduction')
                Introductions.append(introduction.text)
            except:
                Introductions.append('')
                continue
            
        data = pd.DataFrame({"title":titles2, "author":authors, introduction":Introductions, "url":urls})

        return data

if __name__ == '__main__':
    mc = BookIntroCrawler()
    mc.crawl()