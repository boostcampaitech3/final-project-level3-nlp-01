## melon 가사 크롤러

### 사용법

code 디렉토리에서 용도에 맞는(영화, 공연, 노래) ipynb 파일 사용
- (영화) `movies_find_unused_labels.ipynb`
- (공연) `plays_find_unused_labels.ipynb`
- (노래) `songs_find_unused_labels.ipynb`

### label 추적 과정
각 요소를 pipe에 넣어서 일정 수치(score 0.5) 이상의 label을 최대 5개 뽑고, 해당 요소를 각 label에 포함시켰습니다.
그러므로 같은 영화가 다른 label에 중복되어 포함될 수 있습니다.

### 결과 요약
각 도메인 별로 어떠한 요소도 포함되지 않은 label과 평균 예상치에 미달되는 요소 개수를 가진 label을 뽑았습니다. 
예를 들어 영화 도메인의 경우 총 291개의 영화가 있는데 label은 44개가 존재하므로 균등하게 분포되었을 때 6.xxx개를 가져야 한다고 보고 6개 이하인 영화를 포함하는 label을 추렸습니다.
- (영화)
    - 어떤 영화도 포함되지 않은 감정: </br>
	['지긋지긋', '뿌듯함', '편안/쾌적', '부끄러움', '역겨움/징그러움', '패배/자기혐오', '귀찮음', '죄책감', '부담/안_내킴', '재미없음']
    - 7개 미만(291개 영화/44개 감정=6.xxxx)의 영화가 포함된 감정:</br>
	['불평/불만', '고마움', '우쭐댐/무시함', '한심함', '짜증', '증오/혐오', '흐뭇함(귀여움/예쁨)', '경악', '서러움']
- (공연)
    - 어떤 공연도 포함되지 않은 감정:</br>
	['지긋지긋', '부끄러움', '패배/자기혐오', '귀찮음', '죄책감', '부담/안_내킴', '재미없음']
    - 7개 미만(934개 공연/44개 감정=21.xxxx)의 공연가 포함된 감정:</br>
	['우쭐댐/무시함', '뿌듯함', '편안/쾌적', '공포/무서움', '한심함', '역겨움/징그러움', '증오/혐오', '경악']
- (노래)
    - 어떤 노래도 포함되지 않은 감정: </br>
	['존경', '의심/불신', '부끄러움', '공포/무서움', '귀찮음', '죄책감', '경악', '부담/안_내킴', '재미없음'] </br>
    - 7개 미만(603개 노래/44개 감정=13.xxxx)의 노래가 포함된 감정: </br>
	['지긋지긋', '우쭐댐/무시함', '뿌듯함', '편안/쾌적', '한심함', '역겨움/징그러움', '어이없음', '패배/자기혐오', '증오/혐오', '당황/난처', '놀람']

### 예시
- (영화)
    - 포함한 영화가 없는 label:</br>
    <img width="105" alt="스크린샷 2022-06-02 오전 2 05 59" src="https://user-images.githubusercontent.com/79218038/171461034-0f61fe8e-7118-4630-af8b-f1b798ec96b6.png">
    
    - 포함한 영화가 적은 label:</br>
    <img width="363" alt="스크린샷 2022-06-02 오전 2 05 45" src="https://user-images.githubusercontent.com/79218038/171461021-7e84c0d5-e02e-48a8-86f2-cf6254112038.png">
