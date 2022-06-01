## MongoDB docker
- https://poiemaweb.com/docker-mongodb
- https://www.bmc.com/blogs/mongodb-docker-container/

```bash
# MongoDB image 다운로드
$ docker pull mongo

# MongoDB image 확인
$ docker images

# MongoDB Container 구동
$ docker run --name mongodb-container -v ~/data_db:/data/db -d -p 27017:27017 mongo

# MongoDB Docker 컨테이너 중지
$ docker stop mongodb-container

# MongoDB Docker 컨테이너 시작
$ docker start mongodb-container

# MongoDB Docker 컨테이너 재시작
$ docker restart mongodb-container

# MongoDB Docker 컨테이너 접속
$ docker exec -it mongodb-container bash
```

## melon 가사 크롤러

### 사용법

윈도우, 맥에 따라 crawler.py -> initDrive 함수 내 Chrome Driver 경로 변경해줄 것.

### 2022년 TOP100

`python crawler.py`

#### output

Lyrics_top100.csv

### 2011 ~ 2021년 TOP50

`python crawler_year.py`

#### output

Lyrics_top50_2011.csv, Lyrics_top50_2012.csv, ..., Lyrics_top50_2021.csv
