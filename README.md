## melon top100 가사 크롤러

### 사용법

윈도우, 맥에 따라 crawler.py -> initDrive 함수 내 Chrome Driver 경로 변경해줄 것.

```python
from crawler import MusicLyricsCrawler
mc = MusicLyricsCrawler()
mc.crawl()
```

### output

Lyrics_top100.csv

```python
from crawler_year import MusicLyricsCrawler
mc = MusicLyricsCrawler()
mc.crawl()
```

### output

Lyrics_top50_2021.csv
Lyrics_top50_2020.csv
...
Lyrics_top50_2011.csv
