from multiprocessing.sharedctypes import Value
from turtle import onclick
import streamlit as st
import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry
from typing import List, Tuple
# import base64  # 나중에 이미지 업로드 용
from multiapp import MultiApp

app = MultiApp()
app.add_app("Foo", foo)

app.run()

def foo():
    st.markdown("test", unsafe_allow_html=True)

####### style
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300&family=Song+Myung&display=swap');

.title{
  font-family: 'Noto Serif KR', serif;
  text-align: center; 
  font-size: 45px;
  color: #343138;
}
.sub_title{
    font-family: 'Noto Serif KR', serif;
    text-align: center;
    font-size: 18px;
    color: #DBA96D;
}
.content{
    font-size: 18px;
}
.box_title{
    font-size: 18px;
    margin: 5px;
}
.box_content{
    font-size: 16px;
    margin: 5px;
}
.emotions{
    font-size: 20px;
    color: #E5A199;
    text-align: center; 
    padding-bottom: 20px;
}
.what{
    font-size: 15px;
    color: #E2B79A;
    text-align: center;
    margin-top: 25px;
    margin-bottom: 5px;
}
.test{
    background-color:yellow;
}
.div1{
    flex-directon: column;
    flex-wrap: wrap;
}
.div2{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    margin: 5px;
}
</style>""", unsafe_allow_html=True)



    ### 필요한 부분들을 미리 선언해둡니다. 
emotions = []
user_label_dict = {}
## 이 부분은 나중에 GET으로 처리예정
KOTE_label = ['불평/불만', '환영/호의', '감동/감탄', '지긋지긋', '고마움', '슬픔', '화남/분노', '존경', '기대감', '우쭐댐/무시함', '안타까움/실망', '비장함', '의심/불신', '뿌듯함', '편안/쾌적', '신기함/관심', '아껴주는', '부끄러움', '공포/무서움', '절망', '한심함', '역겨움/징그러움', '짜증', '어이없음', '없음', '패배/자기혐오', '귀찮음', '힘듦/지침', '즐거움/신남', '깨달음', '죄책감', '증오/혐오', '흐뭇함(귀여움/예쁨)', '당황/난처', '경악', '부담/안_내킴', '서러움', '재미없음', '불쌍함/연민', '놀람', '행복', '불안/걱정', '기쁨', '안심/신뢰']
KOTE_label_dict = {i:KOTE_label[i] for i in range(len(KOTE_label))}
option1, option2, option3 = '', '', ''

def get_feelings_from_diary(user_diary: str) -> List:
    response = requests.post(url="http://localhost:8000/diary/input", json = {"diary_content": user_diary})
    emotions = eval(response.text)
    return emotions

def get_songs_from_emotions(user_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/diary/input", json = {"now_feelings": user_selection})
    playlists = eval(response.text)

def select_emotion_label(temp_data: Tuple) -> List:
    temp_data = return_user_feelings()
    if temp_data[0] == "KOTE":
        final_selection = [x for x, y in zip(KOTE_label, index) if y == True]
    else:
        final_selection = [x for x, y in zip(emotions, index) if y == True]

    return final_selection

# @st.cache(suppress_st_warning=True)
# def return_user_feelings() -> List:
#     global emotions
#     global user_label_dict
#     # print("emotions from get_feelings_from_diary", emotions)
#     emotions = get_feelings_from_diary(user_diary)
#     # print(emotions, len(emotions), type(emotions))

#     st.markdown('<p class="emotions">감정 분석 결과입니다!</p>', unsafe_allow_html=True)
 
#     option1 = st.checkbox(emotions[0])
#     option2 = st.checkbox(emotions[1])
#     option3 = st.checkbox(emotions[2])
#     index = [option1, option2, option3]

#     return ("emotions", index)


global no_emotion
no_emotion = False

###############UI
st.markdown('<p class="title">하루의 마침표.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">오늘을 마무리하기 전, 당신의 감정에 맞는 컨텐츠를 소개해드립니다.</p>', unsafe_allow_html=True)
user_diary = st.text_area(label ="", placeholder = f"오늘 하루는 어떠셨나요? 일기든, 감정을 나타내는 키워드든 자유로운 형식으로 정리해보세요.", height=250)
_, col, _ = st.columns([1]*2+[1])
user_feelings_button = col.button("당신의 감정을 정리해드릴게요", key='user_button')  # st.button은 session_state를 지원하지 않아서 임시방편으로 chckbox를 사용함

### avoiding refresing the entire page when clicking a button
### session state
if 'user_button' not in st.session_state:
    st.session_state.user_button = True

if 'user_button' not in st.session_state:
    st.session_state.user_button = True
# def update_session():
#     st.session_state.update = 

if user_feelings_button:
    st.markdown("***", unsafe_allow_html=True)
    emotions = get_feelings_from_diary(user_diary)

    st.markdown('<p class="emotions">감정 분석 결과입니다!</p>', unsafe_allow_html=True)
    
    _, col2, _ = st.columns([2.7]*2+[1])
    _, col3, _ = st.columns([2.7]*2+[1])
    _, col4, _ = st.columns([2.7]*2+[1])
    col2.checkbox(emotions[0])
    col3.checkbox(emotions[1])
    col4.checkbox(emotions[2])

    st.markdown('<p class="what">원하는 감정을 선택하세요</p>', unsafe_allow_html=True)
    _, col5, _ = st.columns([2]*2+[1])
    recom_button = col5.button("컨텐츠 추천 받기", key='recom_button')

    st.markdown('<p class="what">원하는 감정이 없으신가요?</p>', unsafe_allow_html=True)
    _, col6, _ = st.columns([1.5]*2+[1])
    no_emotions_button = col6.button("원하는 감정이 없어요!", key='no_emo_button')
    # option2 = st.checkbox(emotions[1])
    # option3 = st.checkbox(emotions[2])
    # index = [option1, option2, option3]

    # there_is_no_emotions = st.button("원하는 감정이 없어요!",)
    if no_emotions_button:
        no_emotion = True
        pass

if no_emotion:
        st.markdown('<p class="emotions">원하는 감정을 선택하세요!</p>', unsafe_allow_html=True)



    #     there_is_no_emotions = st.radio(label="원하는 감정이 없다면 아래 radio를 선택하세요!", options=['원하는 감정이 없어요'], key='emotion_checkbox', disabled=False)

    #     for i in range(len(KOTE_label)):
    #         globals()[f'options_{i}'] = st.checkbox(KOTE_label[i])
    #     index = [f'options_{i}' for i in range(len(KOTE_label))]
        # return ("KOTE", index)
    # final_selection = select_emotion_label(emotion_data)
    # print("final_selection: ", final_selection)

    ### TODO: 기록 확인하기 (유저 history data)





    # def main():
    #     # emotions = return_user_feelings(user_feelings_button)
    #     print("emotions: ", emotions)
    #     print("-----------------------------------------------")
    #     # print(user_label_dict)
    #     # print(user_label_dict[0], user_label_dict[1], user_label_dict[2])
    #     # print(f1, f2, f3)
    #     st.write('Select three known variables:')

    #     option_1 = st.checkbox("A")
    #     # option_2 = st.checkbox(emotions[1])
    #     # option_1 = st.multiselect(label = "감정을 골라보세요!", options = emotions)

    #     # print(option_1, option_2, option_3)
    #     # f1, f2, f3 = return_user_feelings(user_feelings_button)
    #     st.write("지금의 감정들이 맞는지 확인한 후 선택해주세요. 만약 없다면 하단의 버튼을 클릭해주세요. ")


    # main()




    # TODO: 사용자 감정을 받아서 checkbox로 출력




    # for i in range(len(emotions)):
    #     user_label_dict[f"options_{i}"] = st.checkbox(emotions[i])

    # print(d)
    # user_contents_selection = st.multiselect(
    #     "지금의 감정들이 맞는지 확인해주세요. 만약 아니라면, 다음을 선택해주세요!",
    #     string
    # )

    # print(user_contents_selection)
    # show_me_other_feelings = st.button("다른 감정들을 보여주세요")

    # if show_me_other_feelings:
    #     for i in range(len(KOTE_label)):
    #         KOTE_label[i] = st.checkbox(KOTE_label[i])

    # st.write("이런 감정들을 선택하셨어요!")
    # ## 사용자의 일기를 분석하여 감정을 보여줍니다. 
    # show_user_feelings = st.multiselect(
    #     "지금 느끼는 감정들을 선택해주세요", string
    # )



    # print(user_contents[1], user_contents[2], user_contents[3])  ## check selection

    # user_contents_selection = ''
    ### radio button만들기

    # TODO 1: 사용자에게 감정 입력 받는 박스 만들기 (입력: 문장, 키워드, 일기 등 -> 출력: 감정 라벨)
    # if user_feeling_button:
    #     print("Hello World!")  # 사용자의 감정을 정리해줍니다. 누가? 모델이.


    # TODO 2: 사용자가 감정을 입력하면 이를 키워드로 나타내는 모델과 연결시키기

    ##










