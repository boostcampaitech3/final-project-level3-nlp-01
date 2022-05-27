from selenium import webdriver
import pandas as pd

class MusicLyricsCrawler:
    def __init__(self) -> None:
        pass
    
    def crawl(self):
        data = []

        music_url = "https://www.melon.com/chart/index.htm"

        print('Initialize Drive')
        driver = self.initDrive(music_url)

        print('Start parsing')
        data = self.parse(driver)

        print('data 수:', len(data))

        print('Save to csv')
        data.to_csv(f"Lyrics_top100.csv", encoding='utf-8')

        return data

    def initDrive(self, music_url):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정

        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_argument('--disable-dev-shm-usage')

        #### 사용하기 전, 절대경로로 수정해주세요.
        #### 구글 크롬 버전 101.
        driver = webdriver.Chrome('/Users/yejin/Yejin_drive/VSC_projects/final-project-level3-nlp-01/src/chromedriver') # Mac M1
        # driver = webdriver.Chrome('./chromedriver.exe') # Window
        driver.get(music_url)

        return driver

    def parse(self, driver):
        titles = driver.find_elements_by_class_name('ellipsis.rank01')
        titles2 = []
        for i in titles:
            titles2.append(i.text)

        del titles2[100:]
        
        singers = driver.find_elements_by_class_name('ellipsis.rank02')
        singers2 = []
        for i in singers:
            singers2.append(i.text)

        del singers2[100:]

        number = []
        songTagList = driver.find_elements_by_id('lst50')
        for i in songTagList:
            number.append(i.get_attribute('data-song-no'))
            
        songTagList = driver.find_elements_by_id('lst100')
        for i in songTagList:
            number.append(i.get_attribute('data-song-no'))

        Lyric = []
        urls = []
        
        for i in number:
            url = "https://www.melon.com/song/detail.htm?songId=" + i
            urls.append(url)
            driver.get(url)
            if i in '33808429':
                Lyric.append('')
                continue
            lyric = driver.find_element_by_class_name('lyric')
            Lyric.append(lyric.text)
            
        print("title : ", len(titles2), ", singer : ", len(singers2), ", lytic : ", len(Lyric))

        data = pd.DataFrame({"title":titles2, "singer":singers2, "lyric":Lyric, "url": urls})

        return data