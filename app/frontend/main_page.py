from tkinter import PAGES
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import string
import base64  # 나중에 이미지 업로드 용
import write_page

# PAGES = {
#     "Write": write_page
# }


st.markdown('<p class="title">하루의 마침표.</p>', unsafe_allow_html=True)
st.markdown('<p class="sub_title">오늘을 마무리하기 전, 당신의 감정에 맞는 컨텐츠를 소개해드립니다.</p>', unsafe_allow_html=True)

_, col, _ = st.columns([2.5]*2+[1.18])
write_button = col.button("일기 쓰러가기")

# if write_button:
#     page = PAGES['Write']
#     page.app()

st.markdown("***", unsafe_allow_html=True)
st.markdown('<p class="content">오늘은 오랜만에 종로를 갔다! 종로에 가서 마라탕 단골집도 가고~ 더웠지만 재밌었던 걸로..^^ 다음에 또 놀러가서 맛있는 거 먹어야겠다! 내일은 열심히 공부를 해보자.</p>', unsafe_allow_html=True)
st.markdown('<p class="emotions">#즐거움 #기쁨 #배부름</p>', unsafe_allow_html=True)
st.markdown('<p class="date">2022년 6월 2일 목요일 19시 35분</p>', unsafe_allow_html=True)
st.markdown('''<div class="box">
    <div class="div2">
        <img class="song_image" src="https://cdnimg.melon.co.kr/cm2/album/images/109/37/474/10937474_20220428225312_500.jpg/melon/resize/120/quality/80/optimize">
        <div class="div1">
            <a class="box_title" href="https://www.melon.com/song/detail.htm?songId=34997078" target="_blank">That That</a>
            <p class="box_singer">싸이</p>
            <p class="box_content">준비하시고 쏘세요 That That I like That 좌 우 위 아래로<br>That That I like That</p>
        </div>
    </div>
    <div><p class="what">노래</p></div>
</div>''', unsafe_allow_html=True)

st.markdown('''<div class="box">
    <div class="div2">
        <img class="song_image" src="https://cdnimg.melon.co.kr/cm2/album/images/109/37/474/10937474_20220428225312_500.jpg/melon/resize/120/quality/80/optimize">
        <div class="div1">
            <a class="box_title" href="https://www.melon.com/song/detail.htm?songId=34997078" target="_blank">That That</a>
            <p class="box_singer">싸이</p>
            <p class="box_content">준비하시고 쏘세요 That That I like That 좌 우 위 아래로<br>That That I like That</p>
        </div>
    </div>
    <div><p class="what">노래</p></div>
</div>''', unsafe_allow_html=True)

st.markdown('''<div class="box">
    <div class="div2">
        <img class="movie_image" src="https://search.pstatic.net/common?type=o&size=174x242&quality=85&direct=true&src=https%3A%2F%2Fs.pstatic.net%2Fmovie.phinf%2F20220516_144%2F1652665409592Chvey_JPEG%2Fmovie_image.jpg%3Ftype%3Dw640_2">
        <div class="div1">
            <a class="box_title" href="https://movie.naver.com/movie/bi/mi/basic.naver?code=192608" target="_blank">범죄도시</a>
            <p class="box_content">가리봉동 소탕작전 후 4년 뒤, 금천서 강력반은 베트남으로 도주한 용의자를 인도받아 오라는 미션을 받는다. 괴물형사 ‘마석도’(마동석)와 ‘전일만’(최귀화) 반장은 현지 용의자에게서 수상함을 느끼고, 그의 뒤에 무자비한 악행을 벌이는 ‘강해상’(손석구)이 있음을 알게 된다. ‘마석도’와 금천서 강력반은 한국...</p>
        </div>
    </div>
    <div><p class="what">영화</p></div>
</div>''', unsafe_allow_html=True)





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
    margin: 5px;
}
.emotions{
    font-size: 20px;
    color: #E5A199;
}
.date{
    font-size: 15px;
    color: grey;
}
.box_singer{
    font-size: 15px;
    color: grey;
    margin: 5px;
}
.what{
    font-size: 15px;
    color: #E2B79A;
    text-align: right;
    padding-right: 5px;
    width: 40px;
}
.box{
    box-sizing: border-box;
    margin-top: 13px;
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
    height: 110px;
}
.movie_image{
    margin-right: 10px;
    height: 130px;
}
</style>""", unsafe_allow_html=True)