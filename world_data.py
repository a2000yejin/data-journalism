import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import altair as alt
import json
import plotly.express as px
from PIL import Image


#CSV 읽기
def load_data(filename):
    data = pd.read_csv(filename)
    return data

#표 그리기
def draw_chart(df_data):
    st.write(pd.DataFrame(df_data))


#홈페이지 타이틀과 설명
st.title("몇 년 뒤... 더 이상 팝콘을 못 먹게 될 수도 있다? 🍿🥺")
st.write("_오리지널, 카라멜, 콘소메, 치즈 …_")
st.write("영화관에 있는 다양한 맛의 팝콘들을 보면 사람들이 팝콘을 얼마나 사랑하고 있는지 알 수 있지. 고소하면서 짭짤한 팝콘은 영화 감상에 있어 필수품이라고.",
        "요즘에는 편의점이나 대형 마트에서도 다양한 마트의 팝콘을 만나볼 수 있지. 그만큼 팝콘은 현재 많은 사람들이 즐겨먹는 간식거리로 자리 잡았어.")
st.write("그러나 어쩌면 10년 후 우리는 더 이상 영화를 볼 때 팝콘을 먹지 못할 수도 있어. 다름 아닌 기후위기 때문에..!")

st.subheader("엥? 기후 위기랑 옥수수가 무슨 상관인데?")
st.write("옥수수(maize)는 기후 변화에 민감한 주식이야. 특히 가뭄과 같은 기후 현상으로 인해 고온 건조한 날씨가 지속될 시 옥수수 생산에 치명적이지.") 
st.write("옥수수가 왕성하게 자라날 수 있는 온도가 높은 시기 (7-8월)에 옥수수를 갈증 나게 하면 옥수수는 참지 않아.")
st.write("무심하게 내버려 두어도 혼자서도 쑥쑥 자라나는 기특한 녀석으로 입 소문이 자자한 옥수수라 괜찮을 줄 알았다고? 방심은 금물. 토양 수분을 가장 많이 필요로 하는 개화기 전후에 가뭄이 온다면 얄짤 없다고.")
climate_change_def = '<p color:Gray;">*기후위기: 기후 변화로 인해 위험이 증가하는 현실을 뜻하는 용어로, 지구의 평균 기온이 점진적으로 상승하면서 전지구적 기후 패턴이 급격하게 변화하는 현상을 통틀어 일컫는 말</p>'
st.markdown(climate_change_def, unsafe_allow_html=True)


st.subheader("가뭄의 시기와 옥수수 생산량")
st.write("다음은 1980년부터 2020년까지 옥수수 최대 생산국인 **미국의 '파머 가뭄 심각도 지수(PDSI)'와 옥수수 생산량 수치야.**")
st.write("가뭄 심각도 지수는 파머 선생님께서 만드신 지수로, 세계적으로 널리 사용돼.",
         "파머 선생님은 가뭄을 일반적으로 사소한 불편 혹은 고통을 발생시키는 수분 부족이 아니라 심한 인명 혹은 재산의 손실을 일으키는 현상으로 최소 2-3개월, 길게는 1년 넘게 수분 부족이 지속되는 현상으로 정의하셨어.",
         "온도 및 강수량 데이터를 사용해 상대적 건조도를 충정한 값으로 -10은 건조, +10은 습윤을 뜻하지.")

st.write("**그래서 가뭄… 지금 얼마나 심각한 건데** 😱")
st.write("PDSI 지수가 뚝 떨어졌던 해가 언제인지 그래프에서 확인해 보지 않을래?")
st.write("1988, 2000, 2012년도에는 육안으로 보아도 PDSI 지수가 눈에 띄게 급락했지. 대가뭄으로 인해 옥수수 생산량이 뚝 떨어지게 된 눈물겨운 시기였어.")        
image0 = Image.open('comparison.png')
st.image(image0)
Drought = pd.read_csv('Drought_PDSI(1895~).csv',encoding='cp949')
Drought = pd.DataFrame(Drought)
Drought.columns = ['Year', 'Annual average', '9-yr average']
Drought = Drought[['Year', 'Annual average']]
Drought = Drought.iloc[91:132]
Drought['Year'] = Drought['Year'].astype('str')
Drought['Annual average']=  Drought['Annual average'].astype('float')
Drought['Year'] = Drought['Year']
Drought.index = Drought['Year'].apply(lambda d: datetime.strptime(d, "%Y"))
Drought = Drought.drop(['Year'], axis=1)

if st.button("가뭄 데이터 자세히"):
    st.line_chart(Drought)

US_Maize = pd.read_csv('US_Maize.csv',  encoding='cp949')
US_Maize = US_Maize.loc[2]
US_Maize = pd.DataFrame(US_Maize)
US_Maize = US_Maize.drop(['국가별'])
US_Maize.columns =['Maize Production (ton)']
US_Maize['Maize Production (ton)'] = US_Maize['Maize Production (ton)'].astype(int)

if st.button("옥수수 생산량 데이터 자세히"):
    st.bar_chart(US_Maize)


# 옥수수 생산량과 가뭄 비교
st.markdown("<hr>", unsafe_allow_html=True)
st.write("2012년 이후로 PDSI 지수가 급락하진 않은 것 같아 안심하긴 이르다고. 사실상 미국에선 2000년부터 2022년까지 23년 간 대가뭄이 지속되는 추세야.")
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
                           range_color=(0, 2000)
                          )
fig3.update_layout(autosize=False, margin={"r":0,"t":0,"l":0,"b":0}, width=1000)
st.write(fig3)






