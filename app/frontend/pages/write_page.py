import streamlit as st
import requests
from typing import List, Tuple, Optional, Dict
import random
import copy

# st.sidebar.markdown("# page1")


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
.recom_music{
    text-size: 20px;
    color: #E2B79A;
    margin-bottom: 5px;
    margin-left: 10px;
}
.what_book{
    font-size: 15px;
    color: #B38EB9;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.recom_book{
    text-size: 20px;
    color: #B38EB9;
    margin-bottom: 5px;
    margin-left: 10px;
    margin-top: 10px;
}
.what_movie{
    font-size: 15px;
    color: #ECCB3F;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.recom_movie{
    text-size: 20px;
    color: #ECCB3F;
    margin-bottom: 5px;
    margin-left: 10px;
    margin-top: 10px;
}
.what_play{
    font-size: 15px;
    color: #A5C7A1;
    text-align: right;
    padding-right: 5px;
    width: 35px;
}
.recom_play{
    text-size: 20px;
    color: #A5C7A1;
    margin-bottom: 5px;
    margin-left: 10px;
    margin-top: 10px;
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
.end{
    font-family: 'Noto Serif KR', serif;
    text-align: center;
    color: grey;
    font-size: 15px;
    margin-bottom: 2px;
}
.end2{
    font-family: 'Noto Serif KR', serif;
    text-align: center;
    color: grey;
    font-size: 13px;
}
</style>""", unsafe_allow_html=True)



### ????????? ???????????? ?????? ??????????????????. 
emotions = []
user_label_dict = {}
# final_selection = []
## ??? ????????? ????????? GET?????? ????????????
KOTE_label = ['??????/??????', '??????/??????', '??????/??????', '????????????', '?????????', '??????', '??????/??????', '??????', '?????????', '?????????/?????????', '????????????/??????', '?????????', '??????/??????', '?????????', '??????/??????', '?????????/??????', '????????????', '????????????', '??????/?????????', '??????', '?????????', '?????????/????????????', '??????', '????????????', '??????', '??????/????????????', '?????????', '??????/??????', '?????????/??????', '?????????', '?????????', '??????/??????', '?????????(?????????/??????)', '??????/??????', '??????', '??????/???_??????', '?????????', '????????????', '?????????/??????', '??????', '??????', '??????/??????', '??????', '??????/??????']
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


def check_list_elems_exists(some_list: List) -> List:
    check_list = [int(bool(len(elem))) for elem in some_list]
    check_list_sum = sum(check_list)
    return check_list_sum

def get_feelings_from_diary(user_diary: str) -> Dict:
    response = requests.post(url="http://localhost:8000/diary/input", json = {"diary_content": user_diary})
    user_info = response.json()  # json keys: ['record_time', 'diary_content', 'now_feelings'] ?????? ?????? ??????, ??????, ??????; 
    # diary
    return user_info


# def write_page_diary(user_diary: List) -> 

# def write_page_diary()


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
    all_songs_list =[]
    check_length = check_list_elems_exists(temp_songs)

    st.markdown('<p class="recom_music">????????? ?????? ????????? ?????? ??? ???</p>', unsafe_allow_html=True)
    if check_length == 0:
        return temp_rec_songs_list

    elif check_length == 3:
        for song in temp_songs:
            num = random.randrange(0, len(song))
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="song_image" src="https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg">
                    <div class="div1">
                        <a class="box_title" href={song[num]['hyperlink']} target="_blank">{song[num]['title']}</a>
                        <p class="box_singer">{song[num]['singer']}</p>
                        <p class="box_content">{song[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_music">??????</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_songs_list.append({'title': song[num]['title'], 'singer': song[num]['singer'], 'hyperlink': song[num]['hyperlink'], 'preview': song[num]['preview']})
        return temp_rec_songs_list
    
    else:
        for song in temp_songs:
            if len(song) == 0:
                continue
        else:
            all_songs_list.extend(song)
        
        nums = random.sample(range(0, len(all_songs_list)), min(3, len(all_songs_list)))
        for num in nums:
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="song_image" src="https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg">
                    <div class="div1">
                        <a class="box_title" href={song[num]['hyperlink']} target="_blank">{song[num]['title']}</a>
                        <p class="box_singer">{song[num]['singer']}</p>
                        <p class="box_content">{song[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_music">??????</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_songs_list.append({'title': song[num]['title'], 'singer': song[num]['singer'], 'hyperlink': song[num]['hyperlink'], 'preview': song[num]['preview']})
        return temp_rec_songs_list


### Books
@st.cache
def get_books_from_emotions(final_selection: List) -> List:
    response = requests.post(url="http://localhost:8000/contents/books/search", json = {"feelings": final_selection})
    books = eval(response.content.decode('UTF-8'))
    return books


def recommend_books_from_emotions(temp_books: List) -> List:
    temp_rec_books_list = []
    all_books_list = []
    check_length = check_list_elems_exists(temp_books)
    st.markdown('<p class="recom_book">????????? ???????????? ??? ??? ???</p>', unsafe_allow_html=True)
    if check_length == 0:  ## ?????? temp_books??? ???????????? ??? ??????????????? return temp_rec_books_list ????????????!
        return temp_rec_books_list 
    
    elif check_length == 3:  ## ?????? temp_book??? ??? ????????? ?????? ??????????????? for loop + random.randrange
        for book in temp_books:
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
                <div><p class="what_book">???</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_books_list.append({'title': book[num]['title'],'author': book[num]['author'], 'hyperlink': book[num]['hyperlink'], 'image': book[num]['image'], 'preview': book[num]['preview']})
        return temp_rec_books_list

    else:
        for book in temp_books:
            if len(book) == 0:
                continue
            else:
                all_books_list.extend(book)

        nums = random.sample(range(0, len(all_books_list)), min(3, len(all_books_list)))  # list ????????? ??????. ?????? 198?????? book??? ?????????????????? ??? ??? ???????????? [23, 51, 2]??? ??????
        for num in nums:
            if all_books_list[num]['image'] == 'nan':
                play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            else:
                play_image = all_books_list[num]['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play_image}>
                    <div class="div1">
                        <a class="box_title" href={all_books_list[num]['hyperlink']} target="_blank">{all_books_list[num]['title']}</a>
                        <p class="box_singer">{all_books_list[num]['author']}</p>
                        <p class="box_content">{all_books_list[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_book">???</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_books_list.append({'title': all_books_list[num]['title'],'author': all_books_list[num]['author'], 'hyperlink': all_books_list[num]['hyperlink'], 'image': all_books_list[num]['image'], 'preview': all_books_list[num]['preview']})
        return temp_rec_books_list
    

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
    all_movies_list = []
    check_length = check_list_elems_exists(temp_movies)
    st.markdown('<p class="recom_movie">????????? ????????? ?????? ??? ?????? ???????????? ????????? ?????????</p>', unsafe_allow_html=True)
    if check_length == 0:
        return temp_rec_movies_list

    elif check_length == 3:
        for movie in temp_movies:
            num = random.randrange(0, len(movie))
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={movie[num]['image']}>
                    <div class="div1">
                        <a class="box_title" href={movie[num]['hyperlink']} target="_blank">{movie[num]['title']}</a>
                        <p class="box_content">{movie[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_movie">??????</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_movies_list.append({'title': movie[num]['title'], 'hyperlink': movie[num]['hyperlink'], 'image': movie[num]['image'], 'preview': movie[num]['preview']})
        return temp_rec_movies_list
    
    else:
        for movie in temp_movies:
            if len(movie) == 0:
                continue
            
            else:
                all_movies_list.extend(movie)

        nums = random.sample(range(0, len(all_movies_list)), min(3, len(all_movies_list)))   # list ????????? ??????. ?????? 198?????? book??? ?????????????????? ??? ??? ???????????? [23, 51, 2]??? ??????
        for num in nums:
            if all_movies_list[num]['image'] == 'nan':
                play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            else:
                play_image = all_movies_list[num]['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play_image}>
                    <div class="div1">
                        <a class="box_title" href={all_movies_list[num]['hyperlink']} target="_blank">{all_movies_list[num]['title']}</a>
                        <p class="box_content">{all_movies_list[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_movie">??????</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_movies_list.append({'title': all_movies_list[num]['title'], 'hyperlink': all_movies_list[num]['hyperlink'], 'image': all_movies_list[num]['image'], 'preview': all_movies_list[num]['preview']})
        return temp_rec_movies_list


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
    all_plays_list = []
    check_length = check_list_elems_exists(temp_plays)
    st.markdown('<p class="recom_play">????????? ?????? ????????? ????????? ??????</p>', unsafe_allow_html=True)
    if check_length == 0:
        return temp_rec_plays_list

    elif check_length == 3:
        for play in temp_plays:
            num = random.randrange(0, len(play))
            # if play[num]['image'] != 'None':
            #     play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            # else:
            #     play_image = play[num]['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play[num]['image']}>
                    <div class="div1">
                        <a class="box_title" href={play[num]['hyperlink']} target="_blank">{play[num]['title']}</a>
                        <p class="box_content">{play[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_play">?????? ??????</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_plays_list.append( {'title': play[num]['title'], 'hyperlink': play[num]['hyperlink'], 'image': play[num]['image'], 'preview': play[num]['preview']} )
        return temp_rec_plays_list

    else:
        for play in temp_plays:
            if len(play) == 0:
                continue
            else:
                all_plays_list.extend(play)

        nums = random.sample(range(0, len(all_plays_list)), min(3, len(all_plays_list)))
        for num in nums:
            if all_plays_list[num]['image'] == 'nan':
                play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            else:
                play_image = all_plays_list[num]['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play_image}>
                    <div class="div1">
                        <a class="box_title" href={all_plays_list[num]['hyperlink']} target="_blank">{all_plays_list[num]['title']}</a>
                        <p class="box_content">{all_plays_list[num]['preview']}</p>
                    </div>
                </div>
                <div><p class="what_play">?????? ??????</p></div>
            </div>''', unsafe_allow_html=True)
            temp_rec_plays_list.append( {'title': all_plays_list[num]['title'], 'hyperlink': all_plays_list[num]['hyperlink'], 'image': all_plays_list[num]['image'], 'preview': all_plays_list[num]['preview']} )
        return temp_rec_plays_list


def return_user_info(user_feelings_button=False) -> Dict:
    global emotions
    global user_label_dict

    _, col, _ = st.columns([1.5]*2+[1])
    st.markdown("***", unsafe_allow_html=True)
    user_info = get_feelings_from_diary(user_diary)
    return user_info

def write_diary_and_contents(user_info: Dict, final_rec_contents: List) -> None:
    """
    history/selection/insert?????? ?????? ????????? ????????? ????????????:
    class SelectionInput(BaseModel):
    record_time: str = Field(..., description="???????????? ????????? ??????")
    selected_content: Dict[str, List[Dict[str, str]]] = Field(..., description="????????? ????????????")

    get_feelings_from_diary????????? ?????? ???????????? ???????????????, diary_content, now_feelings??? pop?????? ????????????.
    """ 
    user_info = user_info
    contents = ['songs', 'books', 'movies', 'plays']
    empty_contents = dict.fromkeys(contents)

    user_info['selected_content'] = empty_contents
    

    print("=******************--(*_(-9092374023 user_info")
    print(user_info)
    print(user_info.keys())

    print("===========step2_user_info===========")
    user_info['selected_content'] = empty_contents
    
    for con, fin in zip(contents, final_rec_contents):  # [songs, books, movies, plays]
        if len(fin) == 0:
            user_info['selected_content'][con]=[{},{},{}]
        else:
            user_info['selected_content'][con]= fin
    
    ### user_info ??????
    user_info_for_selection_insert, user_info_for_diary_insert = copy.deepcopy(user_info), copy.deepcopy(user_info)

    user_info_for_selection_insert.pop('now_feelings')
    user_info_for_selection_insert.pop('diary_content')
    print(user_info_for_selection_insert.keys(), "======user_info_for_selection_insert")

    
    print()
    ### user_info ??????
    user_info_for_diary_insert['feelings'] = user_info_for_diary_insert['now_feelings']
    user_info_for_diary_insert.pop('now_feelings')
    user_info_for_diary_insert['recommended_content'] = user_info_for_diary_insert['selected_content']
    user_info_for_diary_insert.pop('selected_content')
    print(user_info_for_diary_insert.keys(), "======user_info_for_selection_insert")


    ### history/selection/insert
    requests.post(url="http://localhost:8000/history/selection/insert", json = user_info_for_selection_insert)

    ### history/diary/insert
    requests.post(url="http://localhost:8000/history/diary/insert", json = user_info_for_diary_insert)


def split_and_show_labels(emotion_data, there_is_no_emotions=False) -> Tuple:
    if there_is_no_emotions:
        st.markdown("***", unsafe_allow_html=True)
        st.markdown('<p class="emotions">????????? ?????? ????????? ?????????, ????????? ?????? ?????? ??????????????? ??????????????????!</p>', unsafe_allow_html=True)
        index = []
        for i in range(len(KOTE_label)):
            globals()[f'options_{i}'] = st.checkbox(KOTE_label[i], key=keys_kote[i])
            index.append(globals()[f'options_{i}'])
        return ("KOTE", index)

    else:
        index = [option1, option2, option3]
        return ("emotions", index)

### ????????? emotions 
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


###############UI
st.markdown('<p class="title">????????? ?????????.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">" ????????? ????????? ???????????????. ????????? ?????? ????????? ????????????."</p>', unsafe_allow_html=True)
user_diary = st.text_area(label ="", placeholder = f"?????? ????????? ???????????????? ?????????, ????????? ???????????? ???????????? ???????????? ???????????? ??????????????????.", height=250)
_, col, _ = st.columns([1.1]*2+[1])

user_feelings_button = False
if user_diary:
    user_feelings_button = col.checkbox("????????? ????????? ?????????????????????", value=st.session_state["test1"], key='check1', on_change=flip1)   # st.button??? session_state??? ???????????? ????????? ?????????????????? chckbox??? ?????????
    if user_feelings_button:

        ### ???
        print("============================== final_selection check!")
        user_info = return_user_info(user_feelings_button)  # output = user_info
        emotions = user_info['now_feelings']

        print("step1: ", emotions)
        #st.markdown("***")
        st.markdown('<p class="emotions">?????? ?????? ???????????????! ?????? ??? ????????? ???????????????.</p>', unsafe_allow_html=True)
        st.markdown('<p class="comments">????????? ????????? ?????????! ??? ???????????? ?????? ???????????? ????????? ??? ????????????. ?????? ?????? ??? ????????? ???????????????!</p>', unsafe_allow_html=True)

        # user_feeling ????????????; show_user_feelings() ??????
        _, col1, _ = st.columns([2.7]*2+[1])
        _, col2, _ = st.columns([2.7]*2+[1])
        _, col3, _ = st.columns([2.7]*2+[1])

        option1 = col1.checkbox(emotions[0])
        option2 = col2.checkbox(emotions[1])
        option3 = col3.checkbox(emotions[2])
        index = [option1, option2, option3]
        emotion_data = ("emotions", index)  # ???????????????

        _, column, _ = st.columns([2.7]*2+[1])
        there_is_no_emotions = column.checkbox("????????? ????????? ?????????!", value=st.session_state["test2"], key='check2', on_change=flip2)
        st.markdown("###")
        print(option1, option2, option3)
        print("step2:")

        temp_emotion_data= split_and_show_labels(emotion_data = emotion_data, there_is_no_emotions = there_is_no_emotions)
        print("step3: ", temp_emotion_data)

        final_selection = select_emotion_label(temp_emotion_data)

        # TODO: ???????????? ???????????? ????????? ???????????????!

        print("=================================== Success!!")
        
        if len(final_selection)==3:
            st.markdown(f'<p class="comments">???????????? ?????? ????????? {final_selection[0].strip()}, {final_selection[1].strip()}, {final_selection[2].strip()} ?????????!</p>', unsafe_allow_html=True)
            st.markdown('<p class="emotions">?????? ????????? ???????????? ????????? ???????????? ?????????????????????!</p>', unsafe_allow_html=True)

            temp_songs = get_songs_from_emotions(final_selection)
            temp_books = get_books_from_emotions(final_selection)
            temp_movies = get_movies_from_emotions(final_selection)
            temp_plays = get_plays_from_emotions(final_selection)

            print(f"num of songs for {final_selection[0]}: {len(temp_songs[0])}, num of songs for {final_selection[1]}: {len(temp_songs[1])}, num of songs for {final_selection[2]}: {len(temp_songs[2])}")  # ?????????! 
            print(f"num of books for {final_selection[0]}: {len(temp_books[0])}, num of movies for {final_selection[1]}: {len(temp_books[1])}, num of books for {final_selection[2]}: {len(temp_books[2])}")  # ?????????! 
            print(f"num of movies for {final_selection[0]}: {len(temp_movies[0])}, num of books for {final_selection[1]}: {len(temp_movies[1])}, num of movies for {final_selection[2]}: {len(temp_movies[2])}")  # ?????????! 
            print(f"num of plays for {final_selection[0]}: {len(temp_plays[0])}, num of plays for {final_selection[1]}: {len(temp_plays[1])}, num of plays for {final_selection[2]}: {len(temp_plays[2])}")  # ?????????! 
            rec_songs_list = recommend_songs_from_emotions(temp_songs)
            rec_books_list = recommend_books_from_emotions(temp_books)
            rec_movies_list = recommend_movies_from_emotions(temp_movies)
            rec_plays_list = recommend_plays_from_emotions(temp_plays)
            final_rec_contents = [rec_songs_list, rec_books_list, rec_movies_list, rec_plays_list]

            st.markdown("##")
            col1, col2 = st.columns([5, 1])
            col1.button("?????? ??????????????????!") # 
            save_to_history = col2.checkbox("????????????")

            if save_to_history:
                print("===========user_info===========")
                write_diary_and_contents(user_info, final_rec_contents)

                print("saved to history!")
            else:
                print("stay calm")

        else:
            st.markdown('<p class="emotions">???????????? ????????? ???????????? ???...</p>', unsafe_allow_html=True)
