from http import client
from tkinter import PAGES
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import random
import webbrowser
# from bokeh.models.widgets import Div

# st.sidebar.markdown("#mainpage")

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
.title_img{
    width: 100%;
    margin-bottom: 100px;
    margin-top: 30px;
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




def get_diary():
    diary = requests.get(url="http://localhost:8000/history/diary")
    diary_history = eval(diary.content.decode('UTF-8'))
    return diary_history

def get_history():
    diary = requests.get(url="http://localhost:8000/history/selection")
    diary_history = eval(diary.content.decode('UTF-8'))
    return diary_history


st.markdown('<p class="title">????????? ?????????.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">???????????? ????????? ???????????????. ????????? ?????? ????????? ????????????.???</p>', unsafe_allow_html=True)

_, col, _ = st.columns([2.5]*2+[1.18])
write_button = col.button("?????? ????????????")

st.markdown('<img class ="title_img" src="https://velog.velcdn.com/images/leeyejin1231/post/372b949a-afd4-4e30-a5c9-50c94123d681/image.png"/>', unsafe_allow_html=True)

if write_button:
    # url = st.get_url()
    link = 'http://118.67.131.239:30001/write_page'
    webbrowser.open_new_tab(link)

diarys = get_diary()
historys = get_history()
historys = historys[6:]
diarys = diarys[6:]
historys.reverse()
diarys.reverse()


for num in range(len(historys)):
    try:
        times = historys[num]['record_time']
        selected_contents = historys[num]['selected_content']
        songs = selected_contents['songs']
        books = selected_contents['books']
        movies = selected_contents['movies']
        plays = selected_contents['plays']
        diary_content = diarys[num]['diary_content']
        feelings = diarys[num]['feelings']
        record_time = diarys[num]['record_time']

        st.markdown(f'<p class="content">{diary_content}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="emotions">#{feelings[0]} #{feelings[1]} #{feelings[2]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="date">{times}</p>', unsafe_allow_html=True)
        
        # ??????
        st.markdown('<p class="recom_music">????????? ?????? ????????? ?????? ??? ???</p>', unsafe_allow_html=True)
        for song in songs:
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="song_image" src="https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg">
                    <div class="div1">
                        <a class="box_title" href={song['hyperlink']} target="_blank">{song['title']}</a>
                        <p class="box_singer">{song['singer']}</p>
                        <p class="box_content">{song['preview']}</p>
                    </div>
                </div>
                <div><p class="what_music">??????</p></div>
            </div>''', unsafe_allow_html=True)

        # ???
        st.markdown('<p class="recom_book">????????? ???????????? ??? ??? ???</p>', unsafe_allow_html=True)
        for book in books:
            if book['image'] == 'nan':
                play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            else:
                play_image = book['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play_image}>
                    <div class="div1">
                        <a class="box_title" href={book['hyperlink']} target="_blank">{book['title']}</a>
                        <p class="box_singer">{book['author']}</p>
                        <p class="box_content">{book['preview']}</p>
                    </div>
                </div>
                <div><p class="what_book">???</p></div>
            </div>''', unsafe_allow_html=True)

        #??????
        st.markdown('<p class="recom_movie">????????? ????????? ?????? ??? ?????? ???????????? ????????? ?????????</p>', unsafe_allow_html=True)
        for movie in movies:
            if movie['image'] == 'nan':
                play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            else:
                play_image = movie['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play_image}>
                    <div class="div1">
                        <a class="box_title" href={movie['hyperlink']} target="_blank">{movie['title']}</a>
                        <p class="box_content">{movie['preview']}</p>
                    </div>
                </div>
                <div><p class="what_movie">??????</p></div>
            </div>''', unsafe_allow_html=True)

        #??????
        st.markdown('<p class="recom_play">????????? ?????? ????????? ????????? ??????</p>', unsafe_allow_html=True)
        for play in plays:
            if play['image'] == 'nan':
                play_image = 'https://icon-library.com/images/no-photo-available-icon/no-photo-available-icon-12.jpg'
            else:
                play_image = play['image']
            st.markdown(f'''<div class="box">
                <div class="div2">
                    <img class="movie_image" src={play_image}>
                    <div class="div1">
                        <a class="box_title" href={play['hyperlink']} target="_blank">{play['title']}</a>
                        <p class="box_content">{play['preview']}</p>
                    </div>
                </div>
                <div><p class="what_play">?????? ??????</p></div>
            </div>''', unsafe_allow_html=True)

        st.markdown("", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
        st.markdown("***", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)

    except:
        continue

st.markdown("<p class='end'>????????? ?????????.</p>", unsafe_allow_html=True)
st.markdown("<p class='end2'>2022 boostcamp AI Tech | nlp-01???</p>", unsafe_allow_html=True)






