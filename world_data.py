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
popcorn_flavour = '<p style = "color:#FFA533;"><em>오리지널, 카라멜, 콘소메, 치즈 …</em></p>'
st.markdown(popcorn_flavour, unsafe_allow_html=True)
st.write("영화관에 있는 다양한 맛의 팝콘들을 보면 사람들이 팝콘을 얼마나 사랑하고 있는지 알 수 있지. 고소하면서 짭짤한 팝콘은 영화 감상에 있어 필수품이라고.")
st.write("그러나 어쩌면 10년 후 우리는 더 이상 영화를 볼 때 팝콘을 먹지 못할 수도 있어. 다름 아닌 기후위기 때문에..!")


st.subheader("엥? 기후 위기랑 팝콘이 무슨 상관인데?")
col1, col2 = st.columns(2)
with col1:
    st.write("팝콘의 주 원료인 옥수수(maize)는 기후 변화에 민감한 주식이야. 특히 가뭄과 같은 기후 현상으로 인해 고온 건조한 날씨가 지속될 시 옥수수 생산에 치명적이지.") 
    st.write("옥수수가 왕성하게 자라날 수 있는 온도가 높은 시기 (7-8월)에 옥수수를 갈증 나게 하면 옥수수는 참지 않아.")
    st.write("무심하게 내버려 두어도 혼자서도 쑥쑥 자라나는 기특한 녀석으로 입 소문이 자자한 옥수수라 괜찮을 줄 알았다고? 방심은 금물. 토양 수분을 가장 많이 필요로 하는 개화기 전후에 가뭄이 온다면 얄짤 없다고.")
    climate_change_def = '<p style = "color:gray;">*기후위기: 기후 변화로 인해 위험이 증가하는 현실을 뜻하는 용어로, 지구의 평균 기온이 점진적으로 상승하면서 전지구적 기후 패턴이 급격하게 변화하는 현상을 통틀어 일컫는 말</p>'
    st.markdown(climate_change_def, unsafe_allow_html=True)
with col2:
    st.image("corn_drought.jpg", width=280)
    


st.subheader("가뭄이 발생한 시기에 옥수수 생산량이 줄어드는 거구나..!")
st.write("맞아. 그런데 시기별로 가뭄이 얼마나 심각했는 지 어떻게 알 수 있냐고? 사람 피부도 지성, 중성, 건성으로 나눌 수 있는 것처럼 가뭄도 건조도에 따라 분류하는 기준이 있어.")
st.write("세계적으로 널리 사용되는 가뭄 지수는  ‘파머 가뭄 심각도 지수(PDSI)’야.",
         "파머 선생님은 가뭄을 심한 인명 혹은 재산의 손실을 일으키는 현상으로 최소 2-3개월, 길게는 1년 넘게 수분 부족이 지속되는 현상으로 정의하셨어.",
         "온도 및 강수량 데이터를 사용해 상대적 건조도를 추정한 값으로 -10은 건조, +10은 습윤을 뜻하지.")

st.subheader("그래서 가뭄… 지금 얼마나 심각한 건데😱")
st.write("그렇다면 1980년부터 2020년까지 옥수수 최대 생산국인 미국의 '파머 가뭄 심각도 지수(PDSI)'와 옥수수 생산량 수치를 살펴보지 않을래?")
st.write("PDSI 지수가 눈에 띄게 높거나 낮았던 해가 언제인지 확인해 보자.")
st.write("우선, 1988, 2012년도에는 PDSI 지수가 눈에 띄게 급락했지. 대가뭄으로 인해 옥수수 생산량이 뚝 떨어지게 된 눈물겨운 시기였어.")
st.write("반대로 1983년, 2000년도에는 PDSI 지수가 대폭 상승했어. 가뭄도 아닌데 옥수수 생산량이 뚝 떨어졌다니 이해가 되지 않는다고? 무엇이든 과유불급이기 마련. 이 시기에는 미국에 대홍수가 일어나 옥수수 생산량에 큰 타격을 입게 된 것이지.")

image0 = Image.open('comparison.png')
st.image(image0)
caption1 = '<p style = "color:gray;"><캡션: 1980-2020년 미국 PDSI 지수와 옥수수 생산량(단위: 1억톤)></p>'
st.markdown(caption1, unsafe_allow_html=True)
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
    caption9 = '<p style = "color:gray;"><캡션: 1980-2020년 미국 PDSI 지수></p>'
    st.markdown(caption9, unsafe_allow_html=True)

US_Maize = pd.read_csv('US_Maize.csv',  encoding='cp949')
US_Maize = US_Maize.loc[2]
US_Maize = pd.DataFrame(US_Maize)
US_Maize = US_Maize.drop(['국가별'])
US_Maize.columns =['Maize Production (ton)']
US_Maize['Maize Production (ton)'] = US_Maize['Maize Production (ton)'].astype(int)

if st.button("옥수수 생산량 데이터 자세히"):
    st.bar_chart(US_Maize)
    caption10 = '<p style = "color:gray;"><캡션: 1980-2020년 미국 옥수수 생산량 (단위:톤)></p>'
    st.markdown(caption10, unsafe_allow_html=True)

# 옥수수 생산량과 가뭄 비교
st.markdown("<hr>", unsafe_allow_html=True)
st.write("2012년 이후로 옥수수 생산량이 안정적인 것 같다고 안심하긴 일러. 사실상 미국에선 2000년부터 2022년까지 23년 간 대가뭄이 지속되는 추세야.")
st.write("미국 남서부 지역에서는 주기적으로 가뭄을 겪어왔지만, 20년을 주기로 완화되는 경향을 보였어.",
         "그런데, 이번 가뭄은 20년이 넘도록 미국을 괴롭혀 와, 1200년 만의 최악의 가뭄으로 여겨지고 있어.")
st.text("")

selected_item = st.radio("보고싶은 지도를 선택해주세요!",("지역별 가뭄", "지역별 옥수수 생산량", "전년대비 지역별 옥수수 생산량"))	
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
if selected_item == "지역별 가뭄":
    image1 = Image.open('us_drought.png')
    st.image(image1)
    caption2 = '<p style = "color:gray;"><캡션: 미국 지역별 가뭄></p>'
    st.markdown(caption2, unsafe_allow_html=True)
    
elif selected_item == "지역별 옥수수 생산량":
    fig = go.Figure(data=go.Choropleth(
    locations=df['States'], # Spatial coordinates
    z = df['Acres'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'greens',
    colorbar_title = "Acres"
    ))
    fig.update_layout(
        title_text = '주별 옥수수 생산량',
        geo_scope='usa' # limite map scope to USA
    )
    st.write(fig)
    
elif selected_item == "전년대비 지역별 옥수수 생산량":
    fig = go.Figure(data=go.Choropleth(
    locations=df['States'], # Spatial coordinates
    z = df['percent changes'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'viridis',
    colorbar_title = "증감률(%)"
    ))
    fig.update_layout(
        title_text = '전년 대비 지역별 옥수수 생산량 증감률',
        geo_scope='usa' # limite map scope to USA
    )
    st.write(fig)

st.write("더 무서운 건 뭔 지 알아? 이 가뭄이 언제 끝날지 모른다는 점이야. 가뭄이 시작된 지 20년도 넘은 2021년이 최악으로 건조한 해로 기록된 만큼, 전문가들은 가뭄이 앞으로 10년 넘게 이어질 수도 있다고 봐.",
         "듣기만 해도 무시무시한 ‘메가가뭄’이 진행 중인 것이지.")
st.write("실제로 전미 옥수수 생산량 1위를 자랑하던 아이오와주도 대가뭄 앞에선 맥을 못 추리고 있어. 경지 면적의 41%가 메말라 농사를 포기하는 농부들이 속출했어.")
    

#월 평균 세계 기온 정보
st.subheader("정말 큰일이네… 앞으로도 가뭄이 자주 발생할 것 같아?")
st.write("기온이 상승하면 가뭄이 발생할 가능성이 높아져. 기온이 높아 증발량이 많아지면 표면 수분이 줄기 때문이지.",
         "또한 기온이 상승하면 강우량의 변동폭이 커져 극심한 가뭄과 홍수가 많이 발생할 수 있대.")
st.write("그런데 미국뿐 아니라 세계적으로 기온이 오르고 있어. 아래 데이터는 육지의 대기 온도와 해수면 온도를 합친 값이 1951년-1980년 평균으로부터 얼마나 이탈했는지 보여주는 자료야.")
st.write("원하는 지역과 데이터 형식을 선택해서 살펴봐봐. 점점 뜨거워지는 지구를 볼 수 있어.")
st.text("")
total_climate = load_data('climate_change.csv')
multi_select_list = ['World', 'Northern Hemisphere', 'Southern Hemisphere']
multi_select_temp = st.multiselect('지역을 선택해주세요!',
                             multi_select_list, key=1, default=['World'])
df_temp = pd.DataFrame()
caption5 = '<p style = "color:gray;"><캡션: 1951-1980년 평균 기준 지구 온도의 변화폭 (단위: °C)></p>'

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
        st.markdown(caption5, unsafe_allow_html=True)
    elif selected_item == "라인 그래프":
        st.line_chart(df_temp)
        st.markdown(caption5, unsafe_allow_html=True)
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
        st.markdown(caption5, unsafe_allow_html=True)

st.markdown("***")

# 세계 겨울 온도 정보
st.write("겨울 기온이 올라가는 현상이 특히 문제야. 겨울 기온이 상승하면 북반구가 눈으로 얻는 강우량이 줄어들지.",
         "연간 강우량이 일정하더라도 눈이 쌓여 단단해진 층(snowpack)이 줄어들면 수자원 공급에 문제가 생기고 연어 등 다양한 생물의 생태계에 큰 교란이 일어나.",
         "또한 눈이 줄면 지구 복사열이 줄어들어 기후 온난화가 심화되는 악순환이 일어나지.")
caption6 = '<p style = "color:gray;"><캡션: 1951-1980년 평균 기준 겨울 온도의 변화폭 (단위: °C)></p>'
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
    st.markdown(caption6, unsafe_allow_html=True)

if st.button("Northern Hemisphere"):
    show_winter_temp("Northern Hemisphere")
    st.markdown(caption6, unsafe_allow_html=True)

if st.button("Southern Hemisphere"):
    show_winter_temp("Southern Hemisphere")
    st.markdown(caption6, unsafe_allow_html=True)


# ===================
#월 평균 해수면 온도 정보

st.markdown("***")
st.write("아래는 해수면 온도가 1961년-1990년 평균으로부터 얼마나 이탈했는지 보여주는 자료야. 해수면 온도의 변화가 심할수록 극한 기상이 반복되어 가뭄이 심해진대.")
st.text("")
multi_select_list2 = ['World', 'Northern Hemisphere', 'Southern Hemisphere', 'Tropics']
multi_select_sea_temp = st.multiselect('지역을 선택해주세요!',
                             multi_select_list2, key=3, default=['World'])
df_sea_temp = pd.DataFrame()
caption7 = '<p style = "color:gray;"><캡션: 1961-1990년 평균 기준 지구 해수면 온도의 변화폭 (단위: °C)></p>'

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
        st.markdown(caption7, unsafe_allow_html=True)
    elif selected_item == "라인 그래프":
        st.line_chart(df_sea_temp)
        st.markdown(caption7, unsafe_allow_html=True)
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
        st.markdown(caption7, unsafe_allow_html=True)

st.subheader("그러면 벌써 옥수수 생산량이 많이 줄어든 거야?")
st.write("다행히 아직 많이 줄어들 진 않았어! 옥수수의 생산량은 기후 뿐만 아니라 옥수수 품종, 생산 기술력 등 다양한 요인에 영향을 받거든.",
         "현재 옥수수 품종을 개량하거나 재배기술을 발전시키며 옥수수 생산량을 늘리기 위한 노력이 꾸준히 이루어지고 있어.")
st.write('하지만, 그럼에도 기후 위기로 인한 옥수수 생산량 감소는 불가피해 보여.',
         '미국 항공우주국(나사)에 따르면, 현재처럼 대기중 온실가스가 고농도를 유지할 시 10년 안에 밀 생산량은 24%나 감소한다고 해.',
         '요나스 예거마이어 고다드 우주연구소 연구원도 “2014년 이전 기후농업모델로 분석했을 때는 이런 변화가 예측되지 않았다. 옥수수 수확량 감소는 놀라울 정도로 크고 부정적이다.”라고 나사 보도자료에서 밝혔어.')
st.write("따라서 앞으로 가뭄이 빈번하게 발생하고 기후위기가 지속된다면 옥수수 생산량이 급감하여 심각한 식량 부족 사태가 발생할 수 있어. 더 이상 팝콘을 먹느냐 마느냐의 문제가 아니지…")

# 자급률
st.subheader("그래도 우리나라에서 옥수수 많이 자라고 있지..?🌽🙄")
st.write("대답부터 해주자면 전혀.")
st.write("현재 우리나라의 옥수수 자급률*은 7.9%로 매우 낮은 수치야. 우리나라와 자급률이 비슷한 국가로는 콩고와 자메이카가 있어. 특히 자급률 계산 시 사용한 국내 옥수수 생산량에 우리가 먹는 식용 옥수수 뿐만 아니라 가축 사료, 바이오에너지 등에 이용되는 옥수수까지 포함되어 있다는 점을 고려하면, 우리가 실제로 먹는 옥수수와 팝콘은 거의 우리나라에서 재배되지 않는다고 봐도 무방해.")
st.write("아래 지도를 보면 국가별 옥수수 자급률에 따라 색을 다르게 칠해뒀어. 노란색에 가까울 수록 옥수수 자급률이 좋은 편이고 보라색에 가까울 수록 옥수수 자급률이 낮은 편인데, 우리나라를 봐. 아주 진한 보라색이지? 우리나라가 옥수수 소비의 대부분을 수입에 의존하고 있다는 뜻이야.")

sufficiency_def = '<p style = "color:gray;">*옥수수 자급률 = 국내 옥수수 생산량/국내 옥수수 소비량</p>'
st.markdown(sufficiency_def, unsafe_allow_html=True)
st.text("")
with open("countries.geojson") as f:
    countries = json.load(f)

self_sufficiency = pd.read_csv("grain self-sufficiency.csv")
fig3 = px.choropleth(self_sufficiency, geojson=countries, locations='Country', locationmode='country names', color='maize self-sufficiency ratio(production/consumption)',
                           color_continuous_scale="Viridis",
                           range_color=(0, 2000)
                          )
fig3.update_layout(autosize=False, margin={"r":0,"t":0,"l":0,"b":0}, width=1000)
st.write(fig3)

caption8 = '<p style = "color:gray;"><캡션: 세계 옥수수 자급률 (단위: 톤/톤)><br>최대값은 4535가 넘지만  2000을 넘는 국가는 5개고 나머지는 2000 이하이기 때문에 자급률 간 차이를 자세히 보고자 2000 이상은 노란색으로 처리함<br>흰색은 데이터 값이 없는 부분임. 유럽은 EU 통합지역으로 데이터가 주어져 나라별 데이터는 표시하지 못하였지만 우리의 초점은 한국의 낮은 자급률임.</p>'
st.markdown(caption8, unsafe_allow_html=True)
st.text("")

st.write("그럼 우리나라는 어디서 옥수수를 수입해 오는 걸까? 대한무역협회에 따르면 우리나라는 아르헨티나에 이어 미국으로부터 옥수수를 가장 많이 수입하고 있어. 우리가 지금까지 미국의 옥수수 생산량을 살펴본 이유도 미국이 옥수수 생산량 1위 국가이기도 하지만, 우리나라 옥수수 수급에 특히 많은 영향을 끼치고 있는 나라이기 때문이야.")
st.write("이렇게 옥수수의 수입의존도가 높은 상황에서, 한국의 2위 옥수수 수입대상국인 미국이 빈번한 가뭄으로 인해 옥수수 생산량의 감소를 피하지 못한다면 팝콘을 먹으며 영화를 보는 설렘은 물론, 추운 겨울 따뜻한 방에 앉아 옥수수를 먹는 즐거움은 정말로 추억 속으로 사라지게 될 수도 있어.")

st.markdown("***")
st.subheader("나 팝콘 없인 못 살아~! 앞으로 어떻게 하면 될까?")
st.write("나도 팝콘이 사라진 영화관을 상상하고 싶진 않아. 10년 뒤에도 팝콘을 먹으려면 우리 모두 기후위기에 관심을 가져야겠지? 물론 개인이 할 수 있는 노력이 많지는 않지만, 개개인의 행동이 바뀌어야만 정부와 기업의 기후위기 대응 속도가 달라질테니까!")
st.write("더 이상 기후위기는 나와 상관 없는 먼 미래의 일이 아니야. 오늘은 팝콘에 대해서만 이야기했지만, 지구의 온도가 올라가고 가뭄과 같은 이상 기후가 빈번하게 발생할 시 심각한 식량 부족 문제가 확대될 수 있다는 점만 알아줘.")
        
st.text("")        
st.write("맛있는 팝콘이 부디 지구에서 사라지지 않기를 🙏")

st.image("Food-Tank-36-Climate-Orgs.jpeg")

st.text("")   
st.markdown("***")
st.subheader("출처")
with st.expander("출처 보기"):
    st.write("https://www.yna.co.kr/view/AKR20220913051600009")
    st.write("https://www.hani.co.kr/arti/society/environment/1050887.html")
    st.write("https://dream.kotra.or.kr/kotranews/cms/news/actionKotraBoardDetail.do?")
    st.write("https://dream.kotra.or.kr/kotranews/cms/news/actionKotraBoardDetail.do?pageNo=1&pagePerCnt=10&SITE_NO=3&MENU_ID=70&CONTENTS_NO=1&bbsGbn=00&bbsSn=244,322,245,484,246,444,242,505&pNttSn=194436&pStartDt=&pEndDt=&sSearchVal=&pRegnCd=&pNatCd=&pKbcCd=&pIndustCd=&sSearchVal=")
    st.write("https://m.khan.co.kr/world/america/article/202202152233025#c2b")

st.markdown("***")
writers = '<p style = "color:gray;"> 작성자: 데이터 저널리즘 6조😍 - 김예진, 박규리, 송예은, 정은서 </p>'
st.markdown(writers, unsafe_allow_html=True)
