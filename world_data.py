import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import altair as alt
import json
import plotly.express as px


#CSV 읽기
def load_data(filename):
    data = pd.read_csv(filename)
    return data

#표 그리기
def draw_chart(df_data):
    st.write(pd.DataFrame(df_data))


## 홈페이지 타이틀과 설명
#st.title("US 가뭄과 옥수수 사용량 분석 분석")
#st.write(
#    "분석에 사용한 전체 데이터는 다음과 같다. 데이터를 살펴보려면 아래의 <가뭄 데이터 보기> 버튼을 눌러보자."
#)

# 가뭄데이터 테이블 보기
#if st.button("가뭄 데이터 보기"):
#    st.write("### 데이터")
#    st.write("전체 데이터는 1980년 부터 2020년까지의 미국의 강우량을 기록하고 있다.")
#    st.write(pd.DataFrame(df))

    # st.expander는 접고 펼칠 수 있는 박스를 그려준다.
#    with st.expander("데이터 설명"):
        # st.code는 code형식의 데이터를 보여줄 때 사용된다. language='' 옵션을 사용하면 해당 언어에 맞게 칼라코딩을 해준다.
#        st.code(
#            """D0: Abnormal Dry \nD1: asdf \nD2: adsf \nD3: asdf \nD4: asdf
#            """
#        )


# 옥수수 생산량과 가뭄 비교
st.header("옥수수 생산량과 가뭄 비교")
st.write("보고싶은 지도를 선택해주세요!")
selected_item = st.radio("선택", ("지역별 가뭄", "지역별 옥수수 생산량", "전년대비 지역별 옥수수 생산량"))	
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
if selected_item == "지역별 가뭄":
    st.write("미국 지역별 가뭄 (2022.12.06)")
    from PIL import Image
    image1 = Image.open('us_drought.png')
    st.image(image1)
elif selected_item == "지역별 옥수수 생산량":
    st.write("미국 지역별 옥수수 생산량")
    from PIL import Image
    image2 = Image.open('cornyield.png')
    st.image(image2)
elif selected_item == "전년대비 지역별 옥수수 생산량":
    st.write("미국 지역별 전년대비 옥수수 생산량")
    from PIL import Image
    image3 = Image.open('cornyieldcomparison.png')
    st.image(image3)

st.write("가뭄량과 옥수수 생산량 데이터를 겹쳐봅시다! ... 내일까지 interactive하게 구")
    

#월 평균 세계 기온 정보
total_climate = load_data('climate_change.csv')
st.subheader("전 세계 월단위 온도 변화")
st.write("The combined land-surface air and sea-surface water temperature anomaly is given as the deviation from the 1951–1980 mean.")
multi_select_list = ['World', 'Northern Hemisphere', 'Southern Hemisphere']
multi_select_temp = st.multiselect('지역을 선택해주세요!',
                             multi_select_list, key=1)
df_temp = pd.DataFrame()

selected_item = st.radio("데이터 형식을 선택해주세요!", ("표", "라인 그래프", "히트맵"), key=2)	

if multi_select_temp:
    for i in multi_select_temp:
        mask = (total_climate['Entity'] == i)
        i_temp = total_climate[mask][['Entity', 'Date', 'Temperature anomaly']]
        i_temp = i_temp.dropna()
        i_temp['Date'] = i_temp['Date'].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").date())
        i_temp.index = i_temp['Date']
        i_temp = i_temp.drop(['Date', 'Entity'], axis=1)
        i_temp.columns = [f'{i} temperature anomaly']
        df_temp = pd.concat([df_temp, i_temp], axis=1)

    if selected_item == "표":
        draw_chart(df_temp)
    elif selected_item == "라인 그래프":
        st.line_chart(df_temp)
    elif selected_item == "히트맵":
        mask = (total_climate['Entity'].isin(multi_select_temp))
        temp_heatmap = total_climate[mask][['Date', 'Entity', 'Temperature anomaly']]
        temp_heatmap = temp_heatmap.dropna()
        heatmap1_data = pd.pivot_table(temp_heatmap, values='Temperature anomaly', 
                     index=['Entity'], 
                     columns='Date')
        fig1, ax1 = plt.subplots()
        ax1 = sns.heatmap(heatmap1_data, cmap="coolwarm", center=0)
        ax1.set(xlabel="", ylabel="")
        st.write(fig1)

st.markdown("***")

# 세계 겨울 온도 정보
st.write("Winter Temperature anomaly")

def show_winter_temp(region):
    region_temp = total_climate[total_climate['Entity'] == region][['Date', 'Temperature anomaly']]
    region_temp = region_temp.dropna()
    region_temp['Date'] = region_temp['Date'].apply(lambda d: datetime.strptime(d, "%Y-%m-%d"))
    region_temp['month_of_date'] = region_temp['Date'].dt.month
    region_temp_winter = region_temp[region_temp['month_of_date'].isin([1, 2, 12])]
    region_temp_winter.index = region_temp_winter['Date']
    region_temp_winter = region_temp_winter.drop(['Date', 'month_of_date'], axis=1)
    region_temp_winter.columns = [f'{region} winter temperature anomaly']
    st.line_chart(region_temp_winter)

if st.button("World"):
    show_winter_temp("World")

if st.button("Northern Hemisphere"):
    show_winter_temp("Northern Hemisphere")

if st.button("Southern Hemisphere"):
    show_winter_temp("Southern Hemisphere")


# ===================
#월 평균 해수면 온도 정보
st.subheader("전 세계 월단위 해수면 온도 변화")
st.write("This is measured at a nominal depth of 20cm, and given relative to the average temperature from the period of 1961 - 1990.")
multi_select_list2 = ['World', 'Northern Hemisphere', 'Southern Hemisphere', 'Tropics']
multi_select_sea_temp = st.multiselect('지역을 선택해주세요!',
                             multi_select_list2, key=3)
df_sea_temp = pd.DataFrame()

selected_item = st.radio("데이터 형식을 선택해주세요!", ("표", "라인 그래프", "히트맵"), key=4)	

if multi_select_sea_temp:
    for i in multi_select_sea_temp:
        mask = (total_climate['Entity'] == i)
        i_sea_temp = total_climate[mask][['Entity', 'Date', 'monthly_sea_surface_temperature_anomaly']]
        i_sea_temp = i_sea_temp.dropna()
        i_sea_temp['Date'] = i_sea_temp['Date'].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").date())
        i_sea_temp.index = i_sea_temp['Date']
        i_sea_temp = i_sea_temp.drop(['Date', 'Entity'], axis=1)
        i_sea_temp.columns = [f'{i} sea surface temperature anomaly']
        df_sea_temp = pd.concat([df_sea_temp, i_sea_temp], axis=1)

    if selected_item == "표":
        draw_chart(df_sea_temp)
    elif selected_item == "라인 그래프":
        st.line_chart(df_sea_temp)
    elif selected_item == "히트맵":
        mask = (total_climate['Entity'].isin(multi_select_sea_temp))
        sea_temp_heatmap = total_climate[mask][['Date', 'Entity', 'monthly_sea_surface_temperature_anomaly']]
        sea_temp_heatmap = sea_temp_heatmap.dropna()
        heatmap2_data = pd.pivot_table(sea_temp_heatmap, values='monthly_sea_surface_temperature_anomaly', 
                     index=['Entity'], 
                     columns='Date')
        fig2, ax2 = plt.subplots()
        ax2 = sns.heatmap(heatmap2_data, cmap="coolwarm", center=0)
        ax2.set(xlabel="", ylabel="")
        st.write(fig2)

# ==============
# 자급률
with open("countries.geojson") as f:
    countries = json.load(f)

self_sufficiency = pd.read_csv("grain self-sufficiency.csv")
fig3 = px.choropleth(self_sufficiency, geojson=countries, locations='Country', locationmode='country names', color='maize self-sufficiency ratio(production/consumption)',
                           color_continuous_scale="Viridis",
                           range_color=(0, 4535.631111)
                          )
fig3.update_layout(autosize=False, margin={"r":0,"t":0,"l":0,"b":0}, width=1000)
st.write(fig3)






