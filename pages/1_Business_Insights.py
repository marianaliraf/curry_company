# streamlit: name = Business Insights
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from datetime import datetime
import folium
from streamlit_folium import folium_static

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from styles.custom_css import inject_custom_css
from Utils import Utils


st.set_page_config(page_title = '📊 Business View', layout='wide')

#====================================================
#Funções
#====================================================

def order_metric(df):
    kpi = df[['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    kpi.rename(columns={'ID': 'Total de Pedidos'}, inplace=True)
    fig = px.bar(kpi, x='Order_Date', y='Total de Pedidos',
             color_discrete_sequence=['#63b3ed'],
             labels={'Order_Date': '', 'Total de Pedidos': ''})
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='#cbd5e0')
    
    return fig

def traffic_order_share(df):
    kpi = df[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    kpi = kpi[kpi['Road_traffic_density'] != 'NaN']
    kpi.rename(columns={'ID': 'Total_Pedidos'}, inplace=True)
    kpi['Porcentagem_Pedidos'] = kpi['Total_Pedidos'] / kpi['Total_Pedidos'].sum()
    fig = px.pie(kpi, values='Porcentagem_Pedidos', names='Road_traffic_density',
                 color_discrete_sequence=['#2b6cb0', '#3182ce', '#63b3ed', '#bee3f8'])
    fig.update_layout(paper_bgcolor='#0e1117', font_color='#cbd5e0')
    return fig

def traffic_order_city(df):
    kpi = df[['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    
    fig = px.scatter(kpi, x='City', y='Road_traffic_density', size='ID', color='City',
         color_discrete_sequence=['#63b3ed', '#3182ce', '#2b6cb0'],
         labels={'City': '', 'Road_traffic_density': '', 'ID': ''})
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='#cbd5e0')
    return fig

def order_by_week(df):
    df['Week_of_Year'] = df['Order_Date'].dt.strftime('%U')
    kpi = df.groupby('Week_of_Year')['ID'].count().reset_index().rename(columns={'ID': 'Total_Pedidos'})
    fig = px.line(kpi, x='Week_of_Year', y='Total_Pedidos', color_discrete_sequence=['#63b3ed'], labels={'Week_of_Year': '', 'Total_Pedidos': ''})
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='#cbd5e0')
    return fig

def order_share_week(df):
    df1 = df.groupby('Week_of_Year')['ID'].count().reset_index()
    df2 = df.groupby('Week_of_Year')['Delivery_person_ID'].nunique().reset_index()
    kpi = pd.merge(df1, df2, on='Week_of_Year')
    kpi['order_by_deliver'] = kpi['ID'] / kpi['Delivery_person_ID']
    fig = px.line(kpi, x='Week_of_Year', y='order_by_deliver', color_discrete_sequence=['#63b3ed'], labels={'Week_of_Year': '', 'order_by_deliver': ''})
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='#cbd5e0')
    return fig

def location_share(df):
    cols = ['City', 'Road_traffic_density', 'Delivery_location_longitude', 'Delivery_location_latitude']
    kpi = df[cols].groupby(['City', 'Road_traffic_density']).median().reset_index()
    mapa = folium.Map(zoom_start=6)
    for _, row in kpi.iterrows():
        folium.Marker(
            location=[row['Delivery_location_latitude'], row['Delivery_location_longitude']],
            tooltip=f"{row['City']} - {row['Road_traffic_density']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mapa)
    folium_static(mapa, width=1024, height=600)


# Aplica o estilo personalizado
inject_custom_css()

# Leitura e limpeza dos dados
utils = Utils()
dataset_cury = utils.read_dataset('./datasets/train.csv')
dataset_cury = utils.clean_dataset(dataset_cury)
df = dataset_cury.copy()

#====================================================
#Barra Lateral
#====================================================

image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'logo_cury_company.png')
image_path = os.path.abspath(image_path)
image = Image.open(image_path)

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown("""Please filter""")
data_slider = st.sidebar.slider(
    'Select Limit Date',
     value= datetime(2022, 4, 13),
     min_value = df['Order_Date'].min(),
     max_value = df['Order_Date'].max(),
     format= 'DD-MM-YYYY')

traffic_options = st.sidebar.multiselect(
    "Select Traffic Conditions",
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)

weather_options = st.sidebar.multiselect(
    "Select Weather Conditions",
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

#Filtros
linhas_selecionadas = df['Order_Date'] < data_slider
df = df.loc[linhas_selecionadas,:]

linhas_selecionadas = df['Road_traffic_density'].isin( traffic_options )
df = df.loc[linhas_selecionadas,:]

linhas_selecionadas = df['Weatherconditions'].isin( weather_options )
df = df.loc[linhas_selecionadas,:]

st.sidebar.markdown("---")
st.sidebar.markdown('<p class="sidebar-footer">Powered by Comunidade DS</p>', unsafe_allow_html=True)



#====================================================
#Layout Dashboard
#====================================================
st.header("Marketplace - Business Insights", divider="gray")

# Abas para navegação
aba1, aba2, aba3 = st.tabs(["Management View", "Tactical View", "Geographic View"])

with aba1:
    st.markdown("Orders per Day", unsafe_allow_html=True)
    fig = order_metric(df)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Orders by Traffic Type", unsafe_allow_html=True)
        fig = traffic_order_share(df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("Order Volume by City and Traffic", unsafe_allow_html=True)
        fig = traffic_order_city(df)
        st.plotly_chart(fig, use_container_width=True)

           

with aba2:
    with st.container():
        st.markdown("Orders per Week", unsafe_allow_html=True)
        fig = order_by_week(df)
        st.plotly_chart(fig, use_container_width=True)

        

    with st.container():
        st.markdown("Orders per Delivery Person per Week", unsafe_allow_html=True)
        fig = order_share_week(df)
        st.plotly_chart(fig, use_container_width=True)


    

with aba3:
    st.markdown("City Location by Traffic Type", unsafe_allow_html=True)
    location_share(df)
   



