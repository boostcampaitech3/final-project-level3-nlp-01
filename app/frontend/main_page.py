from http import client
from tkinter import PAGES
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import string
import base64  # 나중에 이미지 업로드 용
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
    border-width: 1.5px;
    border-radius: 15px 15px;
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
    flex-wrap: wrap;
}
.div2{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    margin: 5px;
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




def get_diary():
    diary = requests.get(url="http://localhost:8000/history/diary")
    diary_history = eval(diary.content.decode('UTF-8'))
    return diary_history


st.markdown('<p class="title">하루의 마침표.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">오늘을 마무리하기 전, 당신의 감정에 맞는 컨텐츠를 소개해드립니다.</p>', unsafe_allow_html=True)

_, col, _ = st.columns([2.5]*2+[1.18])
write_button = col.button("일기 쓰러가기")

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

    print("\n\n\n=======diary_time : ", diary_time)
    print("\n\n\n=======diary_content : ", diary_content)
    print("\n\n\n=======feelings : ", feelings)
    print("\n\n\n=======song : ", recom_con_songs[0][0])

    st.markdown("***", unsafe_allow_html=True)

    st.markdown(f'<p class="content">{diary_content}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="emotions">#{feelings[0]} #{feelings[1]} #{feelings[2]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="date">{diary_time}</p>', unsafe_allow_html=True)

    st.markdown('<p class="recom">추천 콘텐츠</p>', unsafe_allow_html=True)
    
    # 노래
    for song in recom_con_songs:
        if len(song) == 0:
            continue
        st.markdown(f'''<div class="box">
            <div class="div2">
                <img class="song_image" src=https://cdnimg.melon.co.kr/cm2/album/images/109/37/474/10937474_20220428225312_500.jpg/melon/resize/120/quality/80/optimize">
                <div class="div1">
                    <a class="box_title" href={song[0]['hyperlink']} target="_blank">{song[0]['title']}</a>
                    <p class="box_singer">{song[0]['singer']}</p>
                    <p class="box_content">{song[0]['preview']}</p>
                </div>
            </div>
            <div><p class="what_music">노래</p></div>
        </div>''', unsafe_allow_html=True)

    # 책
    for book in recom_con_books:
        if len(book) == 0:
            continue
        st.markdown(f'''<div class="box">
            <div class="div2">
                <img class="movie_image" src={book[0]['image']}>
                <div class="div1">
                    <a class="box_title" href={book[0]['hyperlink']} target="_blank">{book[0]['title']}</a>
                    <p class="box_singer">{book[0]['author']}</p>
                    <p class="box_content">{book[0]['preview']}</p>
                </div>
            </div>
            <div><p class="what_book">책</p></div>
        </div>''', unsafe_allow_html=True)

    #영화
    for movie in recom_con_movies:
        if len(movie) == 0:
            continue
        st.markdown(f'''<div class="box">
            <div class="div2">
                <img class="movie_image" src={movie[0]['image']}>
                <div class="div1">
                    <a class="box_title" href={movie[0]['hyperlink']} target="_blank">{movie[0]['title']}</a>
                    <p class="box_content">{movie[0]['preview']}</p>
                </div>
            </div>
            <div><p class="what_movie">영화</p></div>
        </div>''', unsafe_allow_html=True)

    #연극
    for play in recom_con_plays:
        if len(play) == 0:
            continue
        st.markdown(f'''<div class="box">
            <div class="div2">
                <img class="movie_image" src={play[0]['image']}>
                <div class="div2">
                    <a class="box_title" href={play[0]['hyperlink']} target="_blank">{play[0]['title']}</a>
                    <p class="box_content">{play[0]['preview']}</p>
                </div>
            </div>
            <div><p class="what_play">연극</p></div>
        </div>''', unsafe_allow_html=True)







