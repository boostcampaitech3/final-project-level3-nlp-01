from statistics import multimode
import streamlit as st
import pandas as pd
import numpy as np
import base64

# set background, use base64 to read local file
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    """
    function to read png file 
    ----------
    bin_file: png -> the background image in local folder
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: scroll;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('/opt/ml/lv3/final_project/final-project-level3-nlp-01/starry_night.jpg')



st.title("당신의 컨텐츠를 골라보세요!")
# st.write("오늘 하루는 어떠셨나요? 일기든, 감정이든 자유로운 형식으로 정리해보세요")

user_feelings = st.text_input("오늘 하루는 어떠셨나요? 일기든, 감정을 나타내는 키워드든 자유로운 형식으로 정리해보세요.", placeholder = f"(일기) 오늘 하루는 상사때문에 기분이 나빴어.")
user_feelings_button = st.button("당신의 감정을 정리해드릴게요!")


# print(user_contents[1], user_contents[2], user_contents[3])  ## check selection

user_contents_selection = ''
### radio button만들기
# TODO1: multi selection
# TODO2: radio button이 처음부터 눌리지 않도록 바꾸기
# TODO Optional: sidebar와 독립적으로 움직이도록 하기!

## 감정 먼저 정리 -> 맞는지 아닌지 확인
## 인스타 피드 형태로 제공할 수 있도록 (일기, 감정 추천 컨텐츠)


## 감정 먼저 셀렉하고

## 그 다음에 맞는지 확인하기

## 그리고나서 



# @st.cache
# if user_feelings_button:
#     user_contents_selection = st.radio("컨텐츠를 선택해주세요.", ("공연 & 영화", "노래", "책"))

# print(user_contents_selection)  # 확인용
# if user_contents_selection == "공연 & 영화":
#     st.write(f"당신의 하루와 닮은 {user_contents_selection}을 추천해드릴게요!")
#     ### 

# elif user_contents_selection == "노래":
#     st.write(f"당신의 하루를 마무리 할 {user_contents_selection}을 추천해드릴게요!")

# else:
#     st.write(f"당신의 감성을 닮은 {user_contents_selection}을 추천해드릴게요!")

### 

# if user_feelings_button:
#     with st.sidebar:
#         add_radio = st.radio(
#             "컨텐츠를 선택해주세요.",
#             ("공연", "노래", "책"))  # radio에서는 multimode를 지원하지 않으므로, 조금 더 살펴봐야함. ㅠㅠ
        

#         if add_radio == user_contents[1]:
#             st.write("hello world!")
    

        
    



# if add_radio == "공연":
#     st.write(f"{user_contents[1]}")
        
    

# TODO 1: 사용자에게 감정 입력 받는 박스 만들기 (입력: 문장, 키워드, 일기 등 -> 출력: 감정 라벨)
# if user_feeling_button:
#     print("Hello World!")  # 사용자의 감정을 정리해줍니다. 누가? 모델이.

# TODO 2: 사용자가 감정을 입력하면 이를 키워드로 나타내는 모델과 연결시키기