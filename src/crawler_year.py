from time import sleep
from selenium import webdriver
import pandas as pd

class MusicLyricsCrawler:
    def __init__(self) -> None:
        pass
    
    def crawl(self):
        data = []
        years = [i for i in range(2011, 2022)]
        # years = [i for i in range(2011, 2022)]
        
        for year in years:
            music_url = "https://www.melon.com/chart/age/index.htm?chartType=YE&chartGenre=KPOP&chartDate="+str(year)

            print('Initialize Drive')
            driver = self.initDrive(music_url)

            print('Start parsing')
            data = self.parse(driver)

            print('data 수:', len(data))

            print('Save to csv')
            data.to_csv(f"Lyrics_top50_{year}.csv", encoding='utf-8', index=False)

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

        del titles2[50:]
        
        singers = driver.find_elements_by_class_name('ellipsis.rank02')
        singers2 = []
        for i in singers:
            singers2.append(i.text)

        del singers2[50:]

        numbers = []
        songTagList = driver.find_elements_by_css_selector('#lst50 > td:nth-child(4) > div > button.btn_icon.play')
        for i in songTagList:
            num = i.get_attribute('onclick')[31:39]
            if num[-1] == ')':
                num = num.replace(')', '')
            numbers.append(num)
        
        urls = []    
        Lyric = []
        for i in numbers:
            url = "https://www.melon.com/song/detail.htm?songId=" + i
            urls.append(url)
            driver.get(url)
            try:
                lyric = driver.find_element_by_class_name('lyric')
                Lyric.append(lyric.text)
            except:
                Lyric.append('')
                continue
            
            
            # sleep(3)
            
        print("title : ", len(titles2), ", singer : ", len(singers2), ", lytic : ", len(Lyric))

        data = pd.DataFrame({"title":titles2, "singer":singers2, "lyric":Lyric, "url":urls})

        return data


if __name__ == '__main__':
    mc = MusicLyricsCrawler()
    mc.crawl()
