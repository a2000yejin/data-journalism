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
with open("countries.geojson") as f:
    countries = json.load(f)

self_sufficiency = pd.read_csv("grain self-sufficiency.csv")
fig3 = px.choropleth(self_sufficiency, geojson=countries, locations='Country', locationmode='country names', color='maize self-sufficiency ratio(production/consumption)',
                           color_continuous_scale="Viridis",
                           range_color=(0, 4535.631111)
                          )
fig3.update_layout(autosize=False, margin={"r":0,"t":0,"l":0,"b":0}, width=1000)
st.write(fig3)




# st.write(type(self_sufficiency['longitude']))
# world_map = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(df)
# st.write(type(self_sufficiency))




# temp_heatmap = total_climate[['Date', 'Entity', 'Temperature anomaly']]
# temp_heatmap = temp_heatmap.dropna()
# temp_heatmap['Date'] = temp_heatmap['Date'].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").year)
# heatmap1_data = pd.pivot_table(temp_heatmap, values='Temperature anomaly', 
#                      index=['Entity'], 
#                      columns='Date')

# fig1, ax = plt.subplots()
# sns.heatmap(heatmap1_data, cmap="coolwarm", center=0)
# st.write(fig1)

# ===============

#월 평균 해수면 온도 정보
# world_sea_surface = world_climate[['monthly_sea_surface_temperature_anomaly']]
# world_sea_surface = world_sea_surface.dropna()

# draw_chart(world_sea_surface)
# st.line_chart(world_sea_surface)

# sea_heatmap = total_climate[['Date', 'Entity', 'monthly_sea_surface_temperature_anomaly']]
# sea_heatmap = sea_heatmap.dropna()
# sea_heatmap['Date'] = sea_heatmap['Date'].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").year)
# heatmap2_data = pd.pivot_table(sea_heatmap, values='monthly_sea_surface_temperature_anomaly', 
#                      index=['Entity'], 
#                      columns='Date')

# fig2, ax = plt.subplots()
# sns.heatmap(heatmap2_data, cmap="coolwarm", center=0)
# st.write(fig2)
# ===============

# world_co2 = world_climate[['Monthly averaged_co2', 'Annual averaged_co2']]
# world_co2 = world_co2.dropna()
# draw_chart(world_co2)
# st.line_chart(world_co2)

# ===============

# total_disasters = load_data("number-of-deaths-from-natural-disasters.csv")
# world_disasters = total_disasters[total_disasters.Entity == 'World']
# world_disasters = world_disasters.drop(columns=['Entity'])
# world_disasters['Year'] = world_disasters['Year'].astype(str)
# # world_disasters.index = world_disasters['Year']
# # world_disasters = world_disasters.drop(['Year'], axis=1)
# world_deaths_by_drought = world_disasters[['Year', 'deaths_drought']]
# world_deaths_by_drought = world_deaths_by_drought.dropna()
# draw_chart(world_deaths_by_drought)

# world_deaths_by_drought_num = world_deaths_by_drought.iloc[:,1].tolist()
# world_deaths_by_drought_year = world_deaths_by_drought.iloc[:,0].tolist()

# world_deaths_by_drought_df = pd.DataFrame({
#     'Year': world_deaths_by_drought_year,
#     'Number of deaths from drought': world_deaths_by_drought_num
# })

# world_deaths_by_drought_alt = alt.Chart(world_deaths_by_drought_df).mark_bar().encode(
#     x='Year',
#     y='Number of deaths from drought'
# )

# st.altair_chart(world_deaths_by_drought_alt, use_container_width=True)





# #인구 csv 읽기
# pop_data = load_data("word_population.csv")
# # print(data.columns)

# #데이터 정리
# pop_data['항목'] = pop_data['항목'].apply(lambda y: y.split()[0])
# pop_data.index = pop_data['항목']

# #총인구, 연간 인구증가율 표
# population_data = pop_data[['총인구', '연간 인구증가율']]
# population_data.rename(columns = {'총인구':'총인구 (100 mil)'}, inplace = True)
# population_data['총인구 (100 mil)'] = population_data['총인구 (100 mil)'] / 100000000
# draw_chart(population_data)

# #총인구 그래프
# #Matplotlib
# # fig, axe = plt.subplots()
# # axe.plot(population_data.index, population_data['총인구'])
# # axe.set_title('World total population 2000-2021 (억)')
# # plt.tick_params(axis='x', which='major', labelsize=5)
# # st.pyplot(fig)

# #Streamlit
# st.line_chart(population_data[["총인구 (100 mil)"]])

# ============== 

# #곡물 데이터 함수
# def crop_data(crop):
#     #csv 읽기
#     crop_data = load_data(f"{crop}.csv")
#     crop_data.index = crop_data['Year']
#     crop_data= crop_data.drop(['Year'], axis=1)
    
    

#     #세계 데이터만
#     world_crop_data = crop_data[crop_data.Country == 'World']
#     world_crop_data = world_crop_data.drop(columns=['Country'])

#     #Production (t) 표
#     world_crop_pro = world_crop_data[['Production (t)']]
#     #데이터 정리
#     world_crop_pro.rename(columns = {'Production (t)':f'{crop} (100 mil t)'}, inplace = True)
#     world_crop_pro[f'{crop} (100 mil t)'] = world_crop_pro[f'{crop} (100 mil t)'] / 100000000

#     #2000년 이후 표
#     from_2000 = world_crop_pro.index >= 2000
#     world_crop_pro_2000 = world_crop_pro[from_2000]
#     # world_maize_production_2000 = world_maize_production.index.astype(int)
#     draw_chart(world_crop_pro_2000)

#     #2000년 이후 그래프
#     st.line_chart(world_crop_pro_2000)

#     return world_crop_data

# #옥수수
# world_maize_data = crop_data("maize")

# #쌀
# world_rice_data = crop_data("rice")

# #밀
# world_wheat_data = crop_data("wheat")

# #주요 작물 총 생산량
# total_pro_list = []
# for i in range(22):
#     total_pro = (world_maize_data.iloc[i]['Production (t)'] + world_rice_data.iloc[i]['Production (t)'] + world_wheat_data.iloc[i]['Production (t)']) / 100000000
#     total_pro_list.append(total_pro)

# total_pro_data = {  
#     'Year':[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],  
#     '3 Major crops production (100 mil t)':total_pro_list
# }

# total_pro_data = pd.DataFrame(total_pro_data)
# total_pro_data.index = total_pro_data['Year']
# total_pro_data= total_pro_data.drop(['Year'], axis=1)
# st.write(total_pro_data)
# st.line_chart(total_pro_data)


# ===============

# #옥수수 csv 읽기
# maize_data = load_data("global-food.csv")
# maize_data['Year'] = maize_data['Year'].astype(int)
# maize_data.index = maize_data['Year']
# maize_data = maize_data.drop(['Year'], axis=1)
# #세계 데이터만
# world_maize_data = maize_data[maize_data.Country == 'World']
# world_maize_data = world_maize_data.drop(columns=['Country'])
# # draw_data(world_maize_data)

# #Production (t) 표
# world_maize_production = world_maize_data[['Production (t)']]
# # draw_chart(world_maize_production)

# #데이터 정리
# world_maize_production.rename(columns = {'Production (t)':'Production (100 mil)'}, inplace = True)
# world_maize_production['Production (100 mil)'] = world_maize_production['Production (100 mil)'] / 100000000

# #2000년 이후 표
# from_2000 = world_maize_production.index >= 2000
# world_maize_production_2000 = world_maize_production[from_2000]
# # world_maize_production_2000 = world_maize_production.index.astype(int)
# draw_chart(world_maize_production_2000)

# #2000년 이후 그래프
# st.line_chart(world_maize_production_2000)

# ==============

# #곡물 생산량/인구 데이터
# year = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
# crop_food_per_person = []

# population_data_2020 = pop_data[['총인구']]
# population_data_2020 = population_data_2020.iloc[:-2 , :]

# world_maize_2020 = world_maize_data[['Food (t)']]
# world_rice_2020 = world_rice_data[['Food (t)']]
# world_wheat_2020 = world_wheat_data[['Food (t)']]
# # st.write(world_maize_2020)
# # st.write(population_data_2020.iloc[3]['총인구'])

# for i in range(20):
#     major_crops = int(world_maize_2020.iloc[i]['Food (t)'] + world_rice_2020.iloc[i]['Food (t)'] + world_wheat_2020.iloc[i]['Food (t)'])
#     value = (major_crops / population_data_2020.iloc[i]['총인구']) * 1000
#     crop_food_per_person.append(value)
# # st.write(maize_pro_per_person)

# #표 만들기
# def create_year_table(acc_year, col, data):
#     year_table = {"Year":acc_year, col : data}
#     year_table = pd.DataFrame(year_table)
#     year_table.index = year_table['Year']
#     year_table = year_table.drop('Year', axis=1)
#     return year_table

# # crop_food_per_person_table = {"Year":year, "Food per person": crop_food_per_person}
# # crop_food_per_person_table = pd.DataFrame(crop_food_per_person_table)
# # crop_food_per_person_table.index = crop_food_per_person_table['Year']
# # crop_food_per_person_table = crop_food_per_person_table.drop('Year', axis=1)

# crop_food_per_person_table = create_year_table(year, "Food per person (kg/person)", crop_food_per_person)

# st.write(crop_food_per_person_table)

# #그래프 그리기
# st.line_chart(crop_food_per_person_table)

# # ===============

# #곡물/인구 증가율
# crop_food_per_person_rate = []
# for i in range(19):
#     rate = ((crop_food_per_person[i+1] - crop_food_per_person[i]) / crop_food_per_person[i]) * 100
#     crop_food_per_person_rate.append(rate)

# # st.write(crop_food_per_person_rate)

# crop_food_per_person_rate_table = create_year_table(year[:-1], "Food per person rate (%)", crop_food_per_person_rate)
# st.write(crop_food_per_person_rate_table)
# st.line_chart(crop_food_per_person_rate_table)