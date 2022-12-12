#!/usr/bin/env python
# coding: utf-8

# In[27]:

import streamlit as st
import pandas as pd
st.title('Drought and Maize Production')


Drought = pd.read_csv('/Users/kyuripark/Desktop/Data Journalism Project/Drought_PDSI(1895~).csv',encoding='cp949')
Drought = pd.DataFrame(Drought)

Drought.columns = ['Year', 'Annual average', '9-yr average']

Drought = Drought[['Year', 'Annual average']]
Drought = Drought.iloc[91:132]
#Drought
Drought['Year'] = Drought['Year'].astype('int')
#Drought['Year'].dtypes
Drought['Year'] = Drought['Year'].astype('int')
Drought['Annual average']=  Drought['Annual average'].astype('float')
#Drought['Annual average'].dtypes

st.dataframe(Drought)

# In[43]:


import matplotlib.pyplot as plt
#import numpy as np

#그래프생성
fig1 = plt.figure(figsize=(20,10))
plt.ylim(-6, 6) #y축 범위
plt.xlabel('Year',fontsize=20) ## x축 라벨 출력
plt.ylabel('PDSI',fontsize=20) ## y축 라벨 출력 
plt.title("Drought") #그래프 이름
plt.plot(Drought['Year'],Drought['Annual average'],color='blue',linestyle='-',marker='o')
st.pyplot(fig1)

# In[45]:


import pandas as pd
US_Maize = pd.read_csv('/Users/kyuripark/Desktop/Data Journalism Project/US_Maize.csv',  encoding='cp949')
US_Maize = US_Maize.loc[2]
US_Maize = pd.DataFrame(US_Maize)


# In[46]:


US_Maize = US_Maize.drop(['국가별'])
US_Maize.columns =['Maize Production']
US_Maize['Maize Production'] = US_Maize['Maize Production'].astype(int)


# In[47]:


import matplotlib.pyplot as plt
xs=US_Maize.index.to_list()			#dy_day(데이터 프레임)의 index(날짜, 시간)를 리스트로 저장 
ys=US_Maize['Maize Production'].to_list()			#dy_day(테이터 프레임)의 volume 필드를 리스트로 저장
fig2 = plt.figure(figsize=(20,10))
plt.xlabel('Year')				#그래프 x축 이름(label) 지정
plt.ylabel('Maize Production')				#그래프 y축 이름(label) 지정
 ## Figure 생성 사이즈는 10 by 10
plt.bar(xs, ys, width=0.6, color='grey')
plt.xticks(rotation = 45)
st.pyplot(fig2)

# In[71]:


import matplotlib.pyplot as plt
import numpy as np

fig3 = plt.figure(figsize=(20,10)) # 그림 사이즈 지정 (가로 14인치, 세로 5인치)
ax1 = fig3.add_subplot(2, 1, 1) # 서브플롯들을 2 x 1 배열로 배치 그중 첫번째
ax2 = fig3.add_subplot(2, 1, 2) # 서브플롯들을 2 x 1 배열로 배치 그중 두번째

ax1.plot(Drought['Year'],Drought['Annual average'],color='blue',linestyle='-',marker='o')
ax1.set_ylim(-6,6)
ax1.set_xlabel('Year')
ax1.set_ylabel('Drought')


ax2.bar(xs, ys, color='deeppink', label='M/T', alpha=0.7, width=0.7)

ax2.set_ylabel('Maize')

plt.xticks(rotation = 45)

st.pyplot(fig3)
