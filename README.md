
# Project Overview

# 하루의 마침표.
### “당신의 하루를 들려주세요. 오늘을 닮은 선물을 드릴게요.”  

```
일기는 편지라기보단 기록입니다. 때문에 하루를 회고하거나 떠오르는 생각을 정리하기 위해 일기를 쓰곤 하죠.
하지만 간혹, 하루를 옮겨적다 보면 누군가 나의 하루에 응답을 보냈으면 좋겠다는 생각을 하기도 합니다. 오늘 하루가 너무도 눈부셔서 자랑을 하고 싶거나, 혹은 반대로 너무나 울적해서 기댈 어깨라도 필요할 때면요.
'하루의 마침표'는 조금 색다른 방식으로 당신의 일기에 답신을 보내기 위해 만들어졌습니다. 우리는 당신의 하루를 듣기 위해, 그리고 오늘을 닮은 선물을 보내기 위해 여기에 있습니다. 
당신의 하루를 나누고 싶은 밤이 찾아올 때면 짤막한 일기를 적어주세요. 우리는 당신의 밤을 책임질 새벽배송을 준비하겠습니다.
```


**하루의 마침표.** 는 일기 텍스트에서 추출된 감정에 기반해 컨텐츠를 추천하는, 그렇게 추천된 컨텐츠와 일기를 합쳐 하나의 완성된 피드로 저장하는 서비스입니다.  

'지금 느끼고 있는 감정을 정의해주세요.' 이런 질문이 들어왔다고 생각해보죠.   
</br>
> ***인기순으로 나열된 컨텐츠 추천 말고, 감정 기반 컨텐츠 추천은 어떨까요?***  

본 프로젝트의 메인 아이디어는 일기를 통해 하루를 대표할 감정을 ! 사용자의 감정을 텍스트로 입력받아 감정을 분석하고, 사용자의 감정을 세 가지로 분류해 알려드립니다. 기본적으로 사용자의 감정과 동일하게 분류된 컨텐츠를 추천해드리지만, 분류된 감정이 사용자의 감정과 맞지 않거나 사용자가 다른 감정을 원하는 경우 다른 감정을 선택할 수 있습니다. 컨텐츠는 사용자가 선택한 최종 3가지의 감정에 기반해 추천됩니다.   
</br>
 
### 하루의 마침표. 프로젝트 미리보기
![overview](https://user-images.githubusercontent.com/82494506/172327794-2b9f6cd4-82c6-4ad9-bba7-c7bebebdeffc.png)
<img width="538" alt="image" src="https://user-images.githubusercontent.com/82494506/172328202-7b4fd268-8dd3-41a9-bbde-52c450759068.png">

사용자가 오늘 하루를 마무리 하는 일기를 쓰게되면, 일기에 맞는 감정 3가지를 추천해 드립니다.  
이때 원하는 감정이 없다면, 목록에서 직접 감정을 선택할 수 있습니다.  
그리고 선택 된 감정 기반으로 다양한 컨텐츠들이 추천됩니다.  
마지막으로 원하는 컨텐츠가 추천되었다면 컨텐츠를 저장할 수 있습니다.


  
</br>
</br>

# Architecture
![Architecture](https://user-images.githubusercontent.com/79088141/172328054-3c7a7c2c-8397-464c-b317-12b43c3d5900.png)
자세한 내용은 [발표 pdf](https://github.com/boostcampaitech3/final-project-level3-nlp-01/files/8851388/NLP_1._.pdf)를 참고해주시면 됩니다.

</br>
</br>

# How to Use

## 가상환경 설정
<br/>다음 링크를 통하여 poetry를 설치합니다.  
https://python-poetry.org/docs<br/>  
그 이후 다음 커맨드를 입력합니다.  
`poetry install`
<br/><br/>

## Pretrained model은 용량이 너무 커서 다음 링크에서 다운받습니다.
#### `https://drive.google.com/drive/folders/1m02-d4Ihl2gdfKoM9iUHqE2AlvdjMhhE?usp=sharing`
<br/><br/>

## Local Server (Front-end, Back-end)

### frontend 실행
1. frontend 모니터링을 위해 새로운 터미널을 실행한 후 다음 커맨드를 차례로 입력합니다.  
    ```console
    source virtualenv.sh
    ```  

    ```console
    cd app/frontend
    ```  

    ```console
    sreamlit run main_page.py
    ```  
    서버환경에서 실행하는 경우 `--server.port {port number}` argument를 추가해주세요. main_page.py 파일명은 추후 수정 예정입니다.   
    
    로컬환경 실행시 Network URL 주소를, 서버환경에서 실행 시 External URL 주소를 클릭하시면 됩니다.  
    ![streamlit_run](https://user-images.githubusercontent.com/38339347/172327893-53a5c403-c76d-4e8e-a2a6-447834599549.png)  


### Back-end 실행
1. 가상환경 활성화를 위해 다음 커맨드를 입력합니다.
    ```console
    source virtualenv.sh```
2. fastapi server를 구동시키기 위해 다음 커맨드를 입력합니다.
    * `python -m app`

    
## Cloud Server
    * `MongoDB` Cloud j서버 
    * `Cloud(GCP`) 또는 `local` 에 서치할 수 있습니다.  

1. MongoDB Docker 실행 
```bash
# MongoDB image 다운로드
$ docker pull mongo

# MongoDB image 확인
$ docker images

# MongoDB Container 구동
$ docker run --name mongodb-container -v ~/data_db:/data/db -d -p 27017:27017 mongo
```

2. MongoDB Data 적재  
```bash
$ python mongo_db_setup.py --url {$GCP IP} --port {port number}
```


## Crawler
크롤러를 사용하기 전, 사용환경에 맞게 Chrome Driver 경로를 변경해주세요.

### melon 가사 크롤러
```bash
# 2022.06 top 100
python crawler.py

# 2011 - 2021 top 50
python crawler_year.py 
```
#### output
Lyrics_top100.csv, Lyrics_top50_2011.csv, Lyrics_top50_2012.csv, ..., Lyrics_top50_2021.csv

# Model
## KcELECTRA(Korean comments ELECTRA)
![ELECTRA](https://user-images.githubusercontent.com/79088141/172328667-8f70b438-3226-4b44-96db-659c552bd45b.png)
![Compare](https://user-images.githubusercontent.com/79088141/172328938-cb56449b-593a-445e-919f-35440df7f8fd.png)  
ELECTRA(Efficiently Learning an Encoder that Classifies Token Replacements Accurately)를 한국어 댓글을 이용하여 학습한 모델이며, 신조어, 오탈자 등 구어체의 특징을 가진 데이터셋으로 훈련되었습니다.  

위 표를 보게되시면, 일반적인 데이터셋에서는 KoELECTRA의 성능이 앞서지만, 구어체가 많은 NSMC에서는 댓글로 학습한 KcELECTRA의 성능이 더 좋았다는 것을 알 수 있습니다.  
Reference : https://github.com/Beomi/KcELECTRA


# Data
'음악', '책', '영화', '공연' 총 네가지 도메인에 대해 `Selenium`을 활용한 web crawling으로 데이터 수집했습니다.  
감정을 분석하는 데에 **소개글**이 필수이므로 크롤링을 진행하며 소개글이 없거나 소개글을 구할 수 없는 데이터는 제외했습니다.  
데이터는 `data` 디렉토리 내 각 도메인 별 디렉토리에 `.csv`로 저장되어 있습니다.  
예를 들어 영화 데이터셋은 `./data/movies/movie_dataset_image.csv` 파일을 이용해 불러올 수 있습니다. ('image'가 포함된 데이터셋을 사용해야 합니다.)
도메인 별 수집 과정은 다음과 같습니다.


## 음악
음악은 2022년 6월 기준 멜론 Top100과 2011 ~ 2021년 동안의 Top50 데이터로 이루어져있습니다.  
수집된 정보는 '제목', '가수', '가사', 'URL', '이미지' 이렇게 다섯가지로 총 600개의 데이터를 확보했습니다.  

<img width="343" alt="music" src="https://user-images.githubusercontent.com/82494506/172329471-ca32221c-ebc2-401e-bc36-135033f05913.png">

## 책
책 데이터는 yes24 소설/시 카테고리 중 '강력추천' 도서 목록((http://www.yes24.com/24/Category/More/001001046?ElemNo=95&ElemSeq=1))을 크롤링했으며 수집된 정보는 '도서명', '저자', '소개글', 'URL', '이미지 경로' 총 다섯가지입니다.  
중복을 제거해 총 238개의 데이터를 확보했습니다.

<img width="200" alt="스크린샷 2022-06-05 오후 9 25 28" src="https://user-images.githubusercontent.com/79218038/172327413-94dc2306-303c-4950-8bd7-935d2e118894.png">


## 영화
영화 데이터는 다음의 경로를 통해 수집되었으며 수집된 정보는 '영화 제목', '소개글', 'URL', '이미지 경로' 총 네가지입니다.  
중복을 제거하여 총 284개의 데이터를 확보했습니다.
- BBC 선정 '2000년 이후 명작 영화 100선'</br><img width="200" alt="스크린샷 2022-06-05 오후 9 37 02" src="https://user-images.githubusercontent.com/79218038/172325968-405cae15-2657-4411-99ce-3ba1e4808cb6.png">


- OTT 플랫폼 별 인기 영화 + 네이버 기준 장르별 많이 검색된 영화</br><img width="200" alt="스크린샷 2022-06-02 오전 2 36 38" src="https://user-images.githubusercontent.com/79218038/172325523-67eae3c5-4225-4cc2-b6fb-52b93d63ee26.png">

- 네이버 영화 랭킹 평점 기준 </br><img width="200" alt="스크린샷 2022-06-05 오후 9 23 21" src="https://user-images.githubusercontent.com/79218038/172325402-0620e2aa-0cde-408e-a53f-8cd81d264257.png">


## 공연
공연 데이터는 네이버 공연 목록에서 '클래식', '뮤지컬', '연극' 등을 포함한 모든 장르를 크롤링했습니다.
상영중/상영예정인 작품을 모두 포함하고 있으며 '공연 제목', '공연 장르', '소개글', 'URL', '이미지 경로' 총 다섯가지 정보를 가지고 있습니다.  
중복을 제거하여 총 300개의 데이터를 확보했습니다.  
<img width="200" alt="스크린샷 2022-06-05 오후 9 24 21" src="https://user-images.githubusercontent.com/79218038/172328587-b4030c2c-ba1a-4f0d-956b-2350620aa682.png">

# Product Serving
프로덕트 서빙 개요는 다음과 같습니다.  
<img width="755" alt="스크린샷 2022-06-07 오후 5 07 25" src="https://user-images.githubusercontent.com/79218038/172329449-d288d97b-408f-4aa3-8756-7af9fa0e3766.png">  
빠르고 간결하게 웹 서비스의 프론트를 만들기 위해 Streamlit을 메인으로 활용했고 HTML, CSS를 추가로 사용했습니다.  
또한 비동기 요청 처리, 빠른 속도, 그리고 api testing의 용이성을 이유로 FastAPI를 사용하여 백엔드를 구성했습니다.

## FrontEnd
<img width="429" alt="스크린샷 2022-06-07 오후 5 08 34" src="https://user-images.githubusercontent.com/79218038/172329680-bb769933-73b8-443b-ab7f-c1187169c594.png">  
  
프론트엔드는 기본적으로 Streamlit을 통해 구현되며 `streamlit.markdown`을 통해 HTML, CSS 문법을 적용하였습니다.  
프론트엔드의 모듈은 다음과 같습니다.
- 일기 텍스트 입력 모듈
- 감정 분류 및 감정 선택 모듈
- 선택된 감정 기반 콘텐츠 추천 모듈
- 완성된 피드(일기+콘텐츠) 저장 모듈

## BackEnd
<img width="271" alt="스크린샷 2022-06-07 오후 5 12 48" src="https://user-images.githubusercontent.com/79218038/172330482-9862599e-bf94-4ddd-9f05-cc593e145f5a.png">  <br/>
<img width="794" alt="스크린샷 2022-06-07 오후 5 12 41" src="https://user-images.githubusercontent.com/79218038/172330501-c566399d-9d71-40ec-8a50-207a634f4f3f.png">  

백엔드는 FastAPI를 활용하여 구성했습니다. 'Diary', 'Contentes', 'History', '기타'로 구성됩니다.  

## Database
<img width="491" alt="image" src="https://user-images.githubusercontent.com/82494506/172334615-d2c2861a-3edc-4429-911a-632c7ec29d16.png">

- GCP Cloud를 사용하여 Local Server와 분리했습니다.
- MongoDB를 사용했습니다.


