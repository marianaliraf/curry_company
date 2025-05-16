# streamlit: name = Restaurant Insights
import pandas as pd
import plotly.express as px
# biblioteca de criação de mapas
import folium
from streamlit_folium import folium_static
from haversine import haversine
from datetime import datetime
from PIL import Image
# construção de dashboards
import streamlit as st
import numpy as np
import plotly.graph_objects as go

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils import Utils
from styles.custom_css import inject_custom_css

# Ajuste de largura do layout principal
st.set_page_config(page_title = 'Restaurant View', layout='wide')




# Aplica o estilo personalizado
inject_custom_css()

# Leitura e limpeza dos dados
utils = Utils()
dataset_cury = utils.read_dataset('./datasets/train.csv')
dataset_cury = utils.clean_dataset(dataset_cury)
df = dataset_cury.copy()

#====================================================
# Função para plotar graficos
#====================================================

def compute_average_distance(df):
    df['distance_km'] = df.apply(
        lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']),
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
        ), axis=1
    )
    return df

def get_restaurant_kpis(df):
    total_delivery_persons = len(df['Delivery_person_ID'].unique())
    avg_distance = np.round(df['distance_km'].mean(), 2)
    cols = ['Time_taken(min)', 'Festival']
    kpi = df[cols].groupby(['Festival']).agg({'Time_taken(min)': ['mean', 'std']})
    kpi.columns = ['Average Time', 'Standard Deviation']
    return total_delivery_persons, avg_distance, kpi

def plot_sunburst_time_by_city_and_traffic(df):
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    grouped = df[cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    grouped.columns = ['Avg Time', 'STD']
    grouped = grouped.reset_index()
    fig = px.sunburst(
        grouped,
        path=['City', 'Road_traffic_density'],
        values='Avg Time',
        color='STD',
        color_continuous_scale='RdBu',
        color_continuous_midpoint=np.average(grouped['STD'])
    )
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
    return fig

def plot_pie_avg_distance_by_city(df):
    avg_distances = df[['City', 'distance_km']].groupby('City').mean().reset_index()
    fig = go.Figure(
        data=[go.Pie(labels=avg_distances['City'], values=avg_distances['distance_km'], pull=[0, 0.05, 0])]
    )
    fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
    return fig

def plot_bar_time_by_city(df):
    grouped = df[['City', 'Time_taken(min)']].groupby('City').agg(['mean', 'std'])
    grouped.columns = ['Avg Time', 'STD']
    grouped = grouped.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Avg Time',
        x=grouped['City'],
        y=grouped['Avg Time'],
        error_y=dict(type='data', array=grouped['STD'])
    ))
    fig.update_layout(barmode='group', plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
    return fig

def show_time_table_by_city_and_traffic(df, styled_table_func):
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    grouped = df[cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    grouped.columns = ['Avg Time', 'STD']
    grouped = grouped.reset_index()
    grouped['Avg Time'] = grouped['Avg Time'].map(lambda x: f"{x:.2f}")
    grouped['STD'] = grouped['STD'].map(lambda x: f"{x:.2f}")
    styled_table_func(grouped)

#====================================================
# Função para aplicar estilo nas tabelas
#====================================================
def styled_table(df):
    df = df.reset_index(drop=True)
    df = df.rename(columns={
        'Delivery_person_ID': 'ID Delivery Man',
        'Delivery_person_Ratings': 'Delivery Average Rating',
        'Road_traffic_density': 'Traffic',
        'Delivery_person_Ratings_media': 'Delivery Man Average Rating',
        'Delivery_person_Ratings_desvio': 'Delivery Man STD',
        'Weatherconditions': 'Weather Conditions',
        'Delivery_mean': 'Delivery Mean',
        'Delivery_std': 'Delivery STD',
        'City': 'Type of City',
        'Time_taken(min)': 'Time Taken (min)'
    })

    # formata todos os valores numéricos como strings com duas casas decimais, centralizados
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].apply(lambda x: f"{x:.2f}".center(10))

    # repete para a coluna "Time Taken (min)" se necessário
    if 'Time Taken (min)' in df.columns:
        df['Time Taken (min)'] = pd.to_numeric(df['Time Taken (min)'], errors='coerce')\
                                     .apply(lambda x: f"{x:.2f}".center(10))

    styled = df.style.set_properties(**{
        'color': '#cbd5e0',
        'border-color': '#2b6cb0'
    }).set_table_styles([
        {
            'selector': 'thead th',
            'props': [
                ('background-color', '#1a202c'),
                ('color', 'white'),
                ('font-weight', 'bold'),
                ('text-align', 'center')
            ]
        }
    ])

    return st.table(styled)



#====================================================
# Barra Lateral
#====================================================
st.header("Marketplace - Restaurant Insights", divider="gray")

image_path = os.path.join('images', 'logo_cury_company.png')
image_path = os.path.abspath(image_path)
st.sidebar.image(image_path, width=120)

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
    ['conditions Cloudy\t', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy\t', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy']
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

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Aplicando Filtros
linhas_selecionadas = df['Order_Date'] < data_slider
df = df.loc[linhas_selecionadas, :]

linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]

linhas_selecionadas = df['Weatherconditions'].isin(weather_options)
df = df.loc[linhas_selecionadas, :]

#====================================================
# Layout Dashboard
#====================================================

# Cálculos principais
df = compute_average_distance(df)
total_delivery_persons, avg_distance, kpi_tempo = get_restaurant_kpis(df)

with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric('Total Delivery Persons', total_delivery_persons)
    col2.metric('Average Distance (km)', avg_distance)
    col3.metric('Avg Time - Festival', np.round(kpi_tempo.loc['Yes', 'Average Time'], 2))
    col4.metric('Std Dev - Festival', np.round(kpi_tempo.loc['Yes', 'Standard Deviation'], 2))
    col5.metric('Avg Time - No Festival', np.round(kpi_tempo.loc['No', 'Average Time'], 2))
    col6.metric('Std Dev - No Festival', np.round(kpi_tempo.loc['No', 'Standard Deviation'], 2))

with st.container():
    st.markdown("""---""")
    st.subheader('Time Distribution')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Average Delivery Time by City and Traffic")
        fig = plot_sunburst_time_by_city_and_traffic(df)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("Average Delivery Distance by City")
        fig = plot_pie_avg_distance_by_city(df)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Time Distribution by City')
        fig = plot_bar_time_by_city(df)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('Time Distribution by City and Traffic')
        show_time_table_by_city_and_traffic(df, styled_table)
