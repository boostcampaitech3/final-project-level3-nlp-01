import streamlit as st
import requests
from typing import List, Tuple, Optional, Dict
import json
import random
from time import strftime
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
    margin-bottom: 50px;
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
    return user_info


### Songs
@st.cache
def get_songs_from_emotions(final_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/contents/songs/search", json = {"feelings": final_selection})
    songs = eval(response.content.decode('UTF-8'))
    #print("============================SONGS====================================")
    #print(songs[0])
    return songs


def recommend_songs_from_emotions(temp_songs: List) -> List:
    temp_rec_songs_list = []
    for song in temp_songs:
        if len(song) == 0:
            continue
        else:
            num = random.randrange(0, len(song))
            print("songs num",num)
            print(song[num])
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="song_image" src=https://thumbs.dreamstime.com/b/dynamic-radial-color-sound-equalizer-design-music-album-cover-template-abstract-circular-digital-data-form-vector-160916775.jpg">
                    <div class="div1">
                        <a class="box_title" href={song[num]['hyperlink']} target="_blank">{song[num]['title']}</a>
                        <p class="box_singer">{song[num]['singer']}</p>
                        <p class="box_content">{song[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_music">노래</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_songs_list.append({'title': song[num]['title'], 'singer': song[num]['singer'], 'hyperlink': song[num]['hyperlink'], 'preview': song[num]['preview']})
    return temp_rec_songs_list  # 수정해야 함! 어떻게 하면 보낼 수 있을까요 ㅠㅠ

### Books
@st.cache
def get_books_from_emotions(final_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/contents/books/search", json = {"feelings": final_selection})
    books = eval(response.content.decode('UTF-8'))
    return books


def recommend_books_from_emotions(temp_books: List) -> List:
    temp_rec_books_list = []
    for book in temp_books:
        if len(book) == 0:
            continue
        else:
            num = random.randrange(0, len(book))
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={book[num]['image']}>
                    <div class="div1">
                        <a class="box_title" href={book[num]['hyperlink']} target="_blank">{book[num]['title']}</a>
                        <p class="box_singer">{book[num]['author']}</p>
                        <p class="box_content">{book[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_book">책</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_books_list.append({'title': book[num]['title'],'author': book[num]['author'], 'hyperlink': book[num]['hyperlink'], 'image': book[num]['image'], 'preview': book[num]['preview']})
            #temp_rec_books_list.append( {'title': book[num]['title'], 'hyperlink': book[num]['hyperlink'], 'image': book[num]['image'], 'preview': book[num]['preview']})
            
    return temp_rec_books_list  # 수정해야 함! 어떻게 하면 보낼 수 있을까요 ㅠㅠ

### Movies
@st.cache
def get_movies_from_emotions(final_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/contents/movies/search", json = {"feelings": final_selection})
    movies = eval(response.content.decode('UTF-8'))
    # print("============================Movies====================================")
    # print(movies[0])
    return movies

def recommend_movies_from_emotions(temp_movies: List) -> List:
    temp_rec_movies_list = []
    i = 0
    for movie in temp_movies:
        if len(movie) == 0:
            continue
        else:
            num = random.randrange(0, len(movie))
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={movie[num]['image']}>
                    <div class="div1">
                        <a class="box_title" href={movie[num]['hyperlink']} target="_blank">{movie[num]['title']}</a>
                        <p class="box_content">{movie[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_movie">영화</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_movies_list.append({'title': movie[num]['title'], 'hyperlink': movie[num]['hyperlink'], 'image': movie[num]['image'], 'preview': movie[num]['preview']})
    return temp_rec_movies_list  # 수정해야 함! 어떻게 하면 보낼 수 있을까요 ㅠㅠ

### Plays
@st.cache
def get_plays_from_emotions(final_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/contents/plays/search", json = {"feelings": final_selection})
    plays = eval(response.content.decode('UTF-8'))
    print("=================check_decode_error=================")
    print(plays)
    return plays


def recommend_plays_from_emotions(temp_plays: List) -> List:
    temp_rec_plays_list = []
    for play in temp_plays:
        if len(play) == 0:
            continue
        else:
            num = random.randrange(0, len(play))
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play[num]['image']}>
                    <div class="div1">
                        <a class="box_title" href={play[num]['hyperlink']} target="_blank">{play[num]['title']}</a>
                        <p class="box_content">{play[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_play">연극 공연</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_plays_list.append( {'title': play[num]['title'], 'hyperlink': play[num]['hyperlink'], 'image': play[num]['image'], 'preview': play[num]['preview']} )
    return temp_rec_plays_list


def return_user_info(user_feelings_button=False) -> List:
    global emotions
    global user_label_dict

    _, col, _ = st.columns([1.5]*2+[1])
    # user_feelings_button = col.checkbox("당신의 감정을 정리해드릴게요", value=st.session_state["test1"], key='check1', on_change=flip1)  # st.button은 session_state를 지원하지 않아서 임시방편으로 chckbox를 사용함
    # print("emotions from get_feelings_from_diary", emotions)
    st.markdown("***", unsafe_allow_html=True)
    user_info = get_feelings_from_diary(user_diary)
    # print(emotions, len(emotions), type(emotions))
 
    return user_info

# 아래 함수는 record_time, diary_content, feelings + 추천컨텐츠를 보내주는 함수임
# def write_diary_and_contents(user_info, final_rec_contents):
#     contents = ['songs', 'books', 'movies', 'plays']
#     empty_contents = dict.fromkeys(contents)
#     ## history에 들어가는 감정은 now_feeling이 아니라서.. feeling으로 바꿔주는 작업 필요
#     user_info['feeling'] = user_info['now_feelings']
#     user_info.pop('now_feelings')
#     user_info['selected_content'] = empty_contents
    

#     for con, fin in zip(contents, final_rec_contents):  # [songs, books, movies, plays]
#         if len(fin) == 0:
#             user_info['selected_content'][con]=[{},{},{}]
#         else:
#             user_info['selected_content'][con]= fin
    
#     user_info = json.dumps(user_info, indent=4)
#     print("***************user_info******************: ", user_info)
#     print("******************done! end of user_info *************")
    
#     requests.post(url="http://localhost:8000/history/selection/insert", json = user_info)

def get_all_contents_from_feelings(user_info: Dict) -> Dict:
    pass




def write_diary_and_contents(user_info, final_rec_contents):
    contents = ['songs', 'books', 'movies', 'plays']
    empty_contents = dict.fromkeys(contents)
    print("===========step1_user_info===========")

    user_info.pop('diary_content')
    user_info.pop('now_feelings')

    print(user_info)
    print(user_info.keys())

    print("===========step2_user_info===========")
    user_info['selected_content'] = empty_contents
    
    for con, fin in zip(contents, final_rec_contents):  # [songs, books, movies, plays]
        if len(fin) == 0:
            user_info['selected_content'][con]=[{},{},{}]
        else:
            user_info['selected_content'][con]= fin
    print("============================================여기!!!")
    print(user_info)
    # user_info = json.dumps(user_info, indent=4)

    print("***************user_info******************: ", user_info)
    print("******************done! end of user_info *************")
    
    requests.post(url="http://localhost:8000/history/selection/insert", json = user_info)


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
st.markdown('<p class="sub_title">" 당신의 하루를 들려주세요. 오늘을 닮은 선물을 드릴게요."</p>', unsafe_allow_html=True)
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
        user_info = return_user_info(user_feelings_button)  # output = user_info
        emotions = user_info['now_feelings']

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
        st.markdown("###")
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
            temp_books = get_books_from_emotions(final_selection)
            temp_movies = get_movies_from_emotions(final_selection)
            temp_plays = get_plays_from_emotions(final_selection)

            print(f"song1: {len(temp_songs[0])}, song2: {len(temp_songs[1])}, song3: {len(temp_songs[2])}")  # 확인용! 나중에 지우기!
            print(f"book1: {len(temp_books[0])}, book2: {len(temp_books[1])}, book3: {len(temp_books[2])}")  # 확인용! 나중에 지우기!
            print(f"movies1: {len(temp_movies[0])}, movie2: {len(temp_movies[1])}, movie3: {len(temp_movies[2])}")  # 확인용! 나중에 지우기!
            print(f"play1: {len(temp_plays[0])}, play2: {len(temp_plays[1])}, play3: {len(temp_plays[2])}")  # 확인용! 나중에 지우기! 
            rec_songs_list = recommend_songs_from_emotions(temp_songs)
            rec_books_list = recommend_books_from_emotions(temp_books)
            rec_movies_list = recommend_movies_from_emotions(temp_movies)
            rec_plays_list = recommend_plays_from_emotions(temp_plays)
            final_rec_contents = [rec_songs_list, rec_books_list, rec_movies_list, rec_plays_list]

            print("check_list from recommeneded list in plays: ", rec_plays_list)
            print("****************************************************")
            print("check_dicts from selected lists: ", rec_songs_list, rec_books_list, rec_movies_list, rec_plays_list)
            st.markdown("##")
            col1, col2 = st.columns([5, 1])
            col1.button("다시 추천해주세요!") # 
            save_to_history = col2.checkbox("저장하기")

            if save_to_history:
                print("--------------------------user_info-------------")
                print(user_info)
                ## TODO: history/diary/insert 호출 후 넣기! 
                ## TODO1: user_info 가져오기 
                ## TODO2: user_info에 selected 추가하기  # songs, books, movies, plays
                write_diary_and_contents(user_info, final_rec_contents)

                print("saved to history!")
            else:
                print("stay calm")

        else:
            st.markdown('<p class="emotions">사용자의 선택을 기다리는 중...</p>', unsafe_allow_html=True)
    ### TODO: 기록 확인하기 (유저 history data)


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