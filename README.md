## melon top100 가사 크롤러

## Pretrained model은 용량이 너무 커서 다음 링크에서 다운받습니다.
#### `https://drive.google.com/drive/folders/1m02-d4Ihl2gdfKoM9iUHqE2AlvdjMhhE?usp=sharing`

## 이후에, app/saved_model 폴더 안에 pytorch_model.bin을 넣어주시면 됩니다.

# APP 실행법
`python -m app`

## melon top100 가사

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
