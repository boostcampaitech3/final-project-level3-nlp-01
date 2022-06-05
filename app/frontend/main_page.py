from http import client
from tkinter import PAGES
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import random
# import write_page

# PAGES = {
#     "Write": write_page
# }


####### style
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300&family=Song+Myung&display=swap');

.title{
  font-family: 'Noto Serif KR', serif;
  text-align: center; 
  font-size: 60px;
  color: #343138;
}
.sub_title{
    font-family: 'Noto Serif KR', serif;
    text-align: center;
    font-size: 20px;
    color: #DBA96D;
    margin-bottom: 50px;
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
    margin-left: 5px;
}
.emotions{
    font-size: 20px;
    color: #E5A199;
    margin-bottom: 3px;
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
.title_img{
    width: 100%;
    margin-bottom: 100px;
    margin-top: 30px;
}
</style>""", unsafe_allow_html=True)




def get_diary():
    diary = requests.get(url="http://localhost:8000/history/diary")
    diary_history = eval(diary.content.decode('UTF-8'))
    return diary_history


st.markdown('<p class="title">하루의 마침표.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">“당신의 하루를 들려주세요. 오늘을 닮은 선물을 드릴게요.”</p>', unsafe_allow_html=True)

_, col, _ = st.columns([2.5]*2+[1.18])
write_button = col.button("일기 쓰러가기")

st.markdown('<img class ="title_img" src="https://velog.velcdn.com/images/leeyejin1231/post/372b949a-afd4-4e30-a5c9-50c94123d681/image.png"/>', unsafe_allow_html=True)

# if write_button:
#     page = PAGES['Write']
#     page.app()

diarys = get_diary()

for diary_history in diarys:

    diary_time = diary_history['record_time']
    diary_content = diary_history['diary_content']
    feelings = diary_history['feelings']
    recommended_contents = diary_history['recommended_content']
    recom_con_songs = recommended_contents["songs"]
    recom_con_books = recommended_contents["books"]
    recom_con_movies = recommended_contents["movies"]
    recom_con_plays = recommended_contents["plays"]

    st.markdown(f'<p class="content">{diary_content}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="emotions">#{feelings[0]} #{feelings[1]} #{feelings[2]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="date">{diary_time}</p>', unsafe_allow_html=True)

    
    # 노래
    if len(recom_con_songs[0]) != 0 or len(recom_con_songs[1]) != 0 or len(recom_con_songs[2]) != 0:
        st.markdown('<p class="recom_music">당신의 밤을 장식할 노래 한 곡</p>', unsafe_allow_html=True)
    for song in recom_con_songs:
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

    # 책
    if len(recom_con_books[0]) != 0 or len(recom_con_books[1]) != 0 or len(recom_con_books[2]) != 0:
        st.markdown('<p class="recom_book">오늘을 마무리할 책 한 권</p>', unsafe_allow_html=True)
    for book in recom_con_books:
        if len(book) == 0:
            continue
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

    #영화
    if len(recom_con_movies[0]) != 0 or len(recom_con_movies[1]) != 0 or len(recom_con_movies[2]) != 0:
        st.markdown('<p class="recom_movie">당신의 하루를 닭은 또 다른 누군가의 하루를 영화로</p>', unsafe_allow_html=True)
    for movie in recom_con_movies:
        if len(movie) == 0:
            continue
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

    #연극
    if len(recom_con_plays[0]) != 0 or len(recom_con_plays[1]) != 0 or len(recom_con_plays[2]) != 0:
        st.markdown('<p class="recom_play">오늘과 닮은 주말을 선물할 공연</p>', unsafe_allow_html=True)
    for play in recom_con_plays:
        if len(play) == 0:
            continue
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

    st.markdown("***", unsafe_allow_html=True)







