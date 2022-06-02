import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import string
import base64  # 나중에 이미지 업로드 용

### h1 -> 제목 크기!

st.markdown("<h1 style='text-align: center;'>하루의 마침표</h1>", unsafe_allow_html=True)
st.markdown("<h4 style= 'text-align: center; color: grey;'>당신의 감정에 맞는 컨텐츠를 소개해드립니다.</h4>", unsafe_allow_html=True)  # TODO: 이 밑에 여백 넣기!
user_diary = st.text_area(label ="", placeholder = f"오늘 하루는 어떠셨나요? 일기든, 감정을 나타내는 키워드든 자유로운 형식으로 정리해보세요.", height=250)


### column 
_, col, _ = st.columns([1.3]*2+[1.18])
user_feelings_button = col.button("당신의 감정을 정리해드릴게요!")

st.markdown("***", unsafe_allow_html=True)

### TODO: 기록 확인하기 (유저 history data)

emotions = []
### 사용자 일기 받아서 respose 받아오기
if user_feelings_button:
    response = requests.post(url = "http://localhost:8000/diary/input", json = {"diary_content": user_diary})
    # print(response)
    #print(response)

# TODO: 사용자 감정을 받아서 checkbox로 출력
    # global emotions
    emotions = eval(response.text)
    print(emotions, len(emotions), type(emotions))

st.write("지금의 감정들이 맞는지 확인한 후 선택해주세요. 만약 아니라면, 아래의 버튼을 눌러주세요!")

### 필요한 부분들을 미리 선언해둡니다. 
user_label_dict = {}
KOTE_label_dict = {}
## 이 부분은 나중에 GET으로 처리예정
KOTE_label = ['불평/불만', '환영/호의', '감동/감탄', '지긋지긋', '고마움', '슬픔', '화남/분노', '존경', '기대감', '우쭐댐/무시함', '안타까움/실망', '비장함', '의심/불신', '뿌듯함', '편안/쾌적', '신기함/관심', '아껴주는', '부끄러움', '공포/무서움', '절망', '한심함', '역겨움/징그러움', '짜증', '어이없음', '없음', '패배/자기혐오', '귀찮음', '힘듦/지침', '즐거움/신남', '깨달음', '죄책감', '증오/혐오', '흐뭇함(귀여움/예쁨)', '당황/난처', '경악', '부담/안_내킴', '서러움', '재미없음', '불쌍함/연민', '놀람', '행복', '불안/걱정', '기쁨', '안심/신뢰']

for i in range(len(emotions)):
    user_label_dict[f"options_{i}"] = st.checkbox(emotions[i])

# print(d)
# user_contents_selection = st.multiselect(
#     "지금의 감정들이 맞는지 확인해주세요. 만약 아니라면, 다음을 선택해주세요!",
#     string
# )

# print(user_contents_selection)
show_me_other_feelings = st.button("다른 감정들을 보여주세요")

if show_me_other_feelings:
    for i in range(len(KOTE_label)):
        KOTE_label[i] = st.checkbox(KOTE_label[i])

st.write("이런 감정들을 선택하셨어요!")
# ## 사용자의 일기를 분석하여 감정을 보여줍니다. 
# show_user_feelings = st.multiselect(
#     "지금 느끼는 감정들을 선택해주세요", string
# )



# print(user_contents[1], user_contents[2], user_contents[3])  ## check selection

user_contents_selection = ''
### radio button만들기

# TODO 1: 사용자에게 감정 입력 받는 박스 만들기 (입력: 문장, 키워드, 일기 등 -> 출력: 감정 라벨)
# if user_feeling_button:
#     print("Hello World!")  # 사용자의 감정을 정리해줍니다. 누가? 모델이.


# TODO 2: 사용자가 감정을 입력하면 이를 키워드로 나타내는 모델과 연결시키기

##