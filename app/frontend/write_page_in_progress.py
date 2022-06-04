import streamlit as st
import requests
from typing import List, Tuple, Optional, Dict
import json
import random
# import base64  # 나중에 이미지 업로드 용
# from multiapp import MultiApp

### page style
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
.comments{
    font-size: 15px;
    color: #E2B79A;
    text-align: center;
    margin-bottom: 25px;
}
.date{
    font-size: 15px;
    color: grey;
}
.box_singer{
    font-size: 15px;
    color: grey;
    margin-left: 5px;
    margin-bottom: 5px;
}
.what_music{
    font-size: 15px;
    color: #E2B79A;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.what_book{
    font-size: 15px;
    color: #B38EB9;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.what_movie{
    font-size: 15px;
    color: #ECCB3F;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.what_play{
    font-size: 15px;
    color: #A5C7A1;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.box{
    box-sizing: border-box;
    margin-bottom: 13px;
    border-style: solid;
    border-color: grey;
    border-width: 0px;
    border-radius: 15px 15px;
    box-shadow: 2px 2px 2px 2px #CCCCCC;
    padding: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.test{
    background-color:yellow;
}
.div1{
    flex-directon: column;
    flex-wrap: nowrap;
}
.div2{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    margin: 5px;
    flex-wrap: nowrap;
}
.song_image{
    margin-right: 10px;
    height: 90px;
}
.movie_image{
    margin-right: 10px;
    height: 100px;
}
.recom{
    text-size: 20px;
    color: #A5C7A1;
    margin-bottom: 5px;
    margin-left: 10px;
}
</style>""", unsafe_allow_html=True)



### 필요한 부분들을 미리 선언해둡니다. 
emotions = []
user_label_dict = {}
# final_selection = []
## 이 부분은 나중에 GET으로 처리예정
KOTE_label = ['불평/불만', '환영/호의', '감동/감탄', '지긋지긋', '고마움', '슬픔', '화남/분노', '존경', '기대감', '우쭐댐/무시함', '안타까움/실망', '비장함', '의심/불신', '뿌듯함', '편안/쾌적', '신기함/관심', '아껴주는', '부끄러움', '공포/무서움', '절망', '한심함', '역겨움/징그러움', '짜증', '어이없음', '없음', '패배/자기혐오', '귀찮음', '힘듦/지침', '즐거움/신남', '깨달음', '죄책감', '증오/혐오', '흐뭇함(귀여움/예쁨)', '당황/난처', '경악', '부담/안_내킴', '서러움', '재미없음', '불쌍함/연민', '놀람', '행복', '불안/걱정', '기쁨', '안심/신뢰']
KOTE_label_dict = {i:KOTE_label[i] for i in range(len(KOTE_label))}

# keys list for KOTE label
keys_kote = [i for i in range(len(KOTE_label))]

# keys list for top 3 label
keys_top3 = ['a','b','c']

## session state; avoiding refresing the entire page when clicking a button 
# callback to update 'test' based on 'check'
def flip1():
    if st.session_state["check1"]:
        st.session_state["test1"] = True
    else:
        st.session_state["test1"] = False

def flip2():
    if st.session_state["check2"]:
        st.session_state["test2"] = True
    else:
        st.session_state["test2"] = False


if "test1" not in st.session_state:
    st.session_state["test1"] = False

if "test2" not in st.session_state:
    st.session_state["test2"] = False



def get_feelings_from_diary(user_diary: str) -> List:
    response = requests.post(url="http://localhost:8000/diary/input", json = {"diary_content": user_diary})
    user_info = response.json()  # json items: ['record_time', 'diary_content', 'now_feelings'] 일기 생성 시간, 내용, 감정; 
    # print(user_info, user_info['now_feelings'], end="\n")
    # print(type(user_info['now_feelings']))
    return user_info['now_feelings']


### 왜 이러는지 모르겠지만 ㅠㅠㅠ
@st.cache
def get_songs_from_emotions(final_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/contents/songs/search", json = {"feelings": final_selection})
    response = eval(response.content)
    return response


# @st.cache(suppress_st_warning=True)
def return_user_feelings(user_feelings_button=False) -> List:
    global emotions
    global user_label_dict

    _, col, _ = st.columns([1.5]*2+[1])
    # user_feelings_button = col.checkbox("당신의 감정을 정리해드릴게요", value=st.session_state["test1"], key='check1', on_change=flip1)  # st.button은 session_state를 지원하지 않아서 임시방편으로 chckbox를 사용함
    # print("emotions from get_feelings_from_diary", emotions)
    st.markdown("***", unsafe_allow_html=True)
    emotions = get_feelings_from_diary(user_diary)
    # print(emotions, len(emotions), type(emotions))
 
    return emotions


def split_and_show_labels(emotion_data, there_is_no_emotions=False) -> Tuple:
    if there_is_no_emotions:
        st.markdown("***", unsafe_allow_html=True)
        st.markdown('<p class="emotions">마음에 드는 감정이 없다면, 원하는 감정 없음 체크박스를 선택해주세요!</p>', unsafe_allow_html=True)
        index = []
        for i in range(len(KOTE_label)):
            globals()[f'options_{i}'] = st.checkbox(KOTE_label[i], key=keys_kote[i])
            index.append(globals()[f'options_{i}'])

        print()
        print("index", index)
        print()
        return ("KOTE", index)
    else:
        index = [option1, option2, option3]
        print(index)
        return ("emotions", index)

### 감정이 emotions 
def select_emotion_label(temp_data: Tuple) -> List:  # 
    # global final_selection
    temp_index = []
    if temp_data[0] == "KOTE":
        temp_index = temp_data[1]
        final_selection = [x for x, y in zip(KOTE_label, temp_index) if y == True]
    elif temp_data[0] == "emotions":
        temp_index = temp_data[1]
        final_selection = [x for x, y in zip(emotions, temp_index) if y == True]
    print("final_selection: ", final_selection)
    return final_selection

### TODO: 감정으로 content를 추천받아오는 함수를 만들어봅니다.
# def get_songs_from_emotions(final_selection: List) -> List:
#     response = requests.post(url="http://localhost:8000/contents/songs/search", json = {"feelings": final_selection})


###############UI
st.markdown('<p class="title">하루의 마침표.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">오늘을 마무리하기 전, 당신의 감정에 맞는 컨텐츠를 소개해드립니다.</p>', unsafe_allow_html=True)
user_diary = st.text_area(label ="", placeholder = f"오늘 하루는 어떠셨나요? 일기든, 감정을 나타내는 키워드든 자유로운 형식으로 정리해보세요.", height=250)
_, col, _ = st.columns([1.1]*2+[1])
### 필요한 사항들
user_feelings_button = False
if user_diary:
    user_feelings_button = col.checkbox("당신의 감정을 정리해드릴게요", value=st.session_state["test1"], key='check1', on_change=flip1)   # st.button은 session_state를 지원하지 않아서 임시방편으로 chckbox를 사용함
    if user_feelings_button:
    # st.markdown('<p class="emotions">감정 분석 결과입니다!</p>', unsafe_allow_html=True)

        ### 여기서부터 테스트
        print("============================== final_selection check!")
        emotions = return_user_feelings(user_feelings_button)  # output = emotions
        print("step1: ", emotions)
        #st.markdown("***")
        st.markdown('<p class="emotions">감정 분석 결과입니다! 감정 세 가지를 골라주세요.</p>', unsafe_allow_html=True)
        st.markdown('<p class="comments">원하는 감정이 없어요! 를 체크하면 다른 감정들을 선택할 수 있습니다. 다른 감정 세 가지를 골라보세요!</p>', unsafe_allow_html=True)

        # user_feeling 보여주기; show_user_feelings() 대체
        _, col1, _ = st.columns([2.7]*2+[1])
        _, col2, _ = st.columns([2.7]*2+[1])
        _, col3, _ = st.columns([2.7]*2+[1])

        option1 = col1.checkbox(emotions[0])
        option2 = col2.checkbox(emotions[1])
        option3 = col3.checkbox(emotions[2])
        index = [option1, option2, option3]
        emotion_data = ("emotions", index)  # 임시데이터

        _, column, _ = st.columns([2.7]*2+[1])
        there_is_no_emotions = column.checkbox("원하는 감정이 없어요!", value=st.session_state["test2"], key='check2', on_change=flip2)

        print(option1, option2, option3)
        print("step2:")

        temp_emotion_data= split_and_show_labels(emotion_data = emotion_data, there_is_no_emotions = there_is_no_emotions)
        print("step3: ", temp_emotion_data)

        final_selection = select_emotion_label(temp_emotion_data)
        print("final_selection: ", final_selection)

        # TODO: 사용자의 감정으로 컨텐츠 추천해오기!

        print("=================================== Success!!")
        
        if len(final_selection)==3:
            st.markdown(f'<p class="comments">사용자가 고른 감정은 {final_selection[0].strip()}, {final_selection[1].strip()}, {final_selection[2].strip()} 이에요!</p>', unsafe_allow_html=True)
            st.markdown('<p class="emotions">최종 선택된 감정으로 다양한 컨텐츠를 추천해드릴게요!</p>', unsafe_allow_html=True)

            temp_songs = get_songs_from_emotions(final_selection)
            print(f"song1: {len(temp_songs[0])}, song2: {len(temp_songs[1])}, song3: {len(temp_songs[2])}")  # 확인용! 나중에 지우기! 
            for song in temp_songs:
                if len(song) == 0:
                    continue
            num = random.randrange(0, len(song))
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="song_image" src=https://cdnimg.melon.co.kr/cm2/album/images/109/37/474/10937474_20220428225312_500.jpg/melon/resize/120/quality/80/optimize">
                    <div class="div1">
                        <a class="box_title" href={song[num]['hyperlink']} target="_blank">{song[num]['title']}</a>
                        <p class="box_singer">{song[num]['singer']}</p>
                        <p class="box_content">{song[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_music">노래</p></div>
            </div>''', unsafe_allow_html=True)

        else:
            st.markdown('<p class="emotions">사용자의 선택을 기다리는 중...</p>', unsafe_allow_html=True)

    #st.markdown("***")
#st.markdown('<p class="emotions">감정 선택이 완료되었으면 다음 버튼을 눌러주세요. </p>', unsafe_allow_html=True)
    

# _, column, _ = st.columns([2.7]*2+[1])
# there_is_no_emotions = column.checkbox("원하는 감정이 없어요!", value=st.session_state["test2"], key='check2', on_change=flip2)

# (there_is_no_emotions)
# emotion_data = show_user_feelings() # -> 이거를 나중에 split and show label로 받기

# temp_emotion_data= split_and_show_labels(emotion_data = emotion_data, there_is_no_emotions = there_is_no_emotions)
# print("step3: ", temp_emotion_data)

# final_selection = select_emotion_label(temp_emotion_data)
# print("final_selection: ", final_selection)
# print("=================================== Success!!")

# if user_feelings_button:
#     st.markdown("***", unsafe_allow_html=True)
#     emotions = get_feelings_from_diary(user_diary)

#     st.markdown('<p class="emotions">감정 분석 결과입니다!</p>', unsafe_allow_html=True)
    
#     _, col2, _ = st.columns([2.7]*2+[1])
#     _, col3, _ = st.columns([2.7]*2+[1])
#     _, col4, _ = st.columns([2.7]*2+[1])
#     col2.checkbox(emotions[0])
#     col3.checkbox(emotions[1])
#     col4.checkbox(emotions[2])

#     st.markdown('<p class="what">원하는 감정을 선택하세요</p>', unsafe_allow_html=True)
#     _, col5, _ = st.columns([2]*2+[1])
#     recom_button = col5.button("컨텐츠 추천 받기", key='recom_button')

#     st.markdown('<p class="what">원하는 감정이 없으신가요?</p>', unsafe_allow_html=True)
#     _, col6, _ = st.columns([1.5]*2+[1])
#     no_emotions_button = col6.button("원하는 감정이 없어요!", key='check', on_change = flip2)
#     option2 = st.checkbox(emotions[1])
#     option3 = st.checkbox(emotions[2])
#     index = [option1, option2, option3]

    # there_is_no_emotions = st.button("원하는 감정이 없어요!",)
    # if no_emotions_button:
    #     no_emotion = True
    #     pass

# if no_emotion:
#         st.markdown('<p class="emotions">원하는 감정을 선택하세요!</p>', unsafe_allow_html=True)



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
