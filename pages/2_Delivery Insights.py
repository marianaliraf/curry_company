# streamlit: name = Delivery Insights
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from haversine import haversine
from datetime import datetime
from PIL import Image
import streamlit as st
import plotly.graph_objects as go

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils import Utils
from styles.custom_css import inject_custom_css

# Ajuste de largura do layout principal
st.set_page_config(page_title = 'Delivery View', layout='wide')


# Aplica o estilo personalizado
inject_custom_css()

# Leitura e limpeza dos dados
utils = Utils()
dataset_cury = utils.read_dataset('./datasets/train.csv')
dataset_cury = utils.clean_dataset(dataset_cury)
df = dataset_cury.copy()

#====================================================
# Função para aplicar estilo nas tabelas
#====================================================
def styled_table(df):
    df = df.reset_index(drop=True)
    df = df.rename(columns={
        'Delivery_person_ID': 'ID Delivery Man',
        'Delivery_person_Ratings': 'Delivery Average Rating',
        'Road_traffic_density': 'Traffic',
        'Delivery_person_Ratings_media': 'Delivry Man Average Rating',
        'Delivery_person_Ratings_desvio': 'Delivry Man STD',
        'Weatherconditions': 'Weather Conditions',
        'Delivery_mean': 'Delivery Mean',
        'Delivery_std': 'Delivery STD',
        'City': 'Type of City',
        'Time_taken(min)': 'Time Taken (min)'
    })
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].map("{:.2f}".format)

    if 'Time Taken (min)' in df.columns:
        df['Time Taken (min)'] = pd.to_numeric(df['Time Taken (min)'], errors='coerce').map("{:.2f}".format)

    styled = df.style.set_properties(**{
        #'background-color': '#1a202c',
        'color': '#cbd5e0',
        'border-color': '#2b6cb0'
    }).set_table_styles([
        {
            'selector': 'thead th',
            'props': [
                ('background-color', '#1a202c'),
                ('color', 'white'),
                ('font-weight', 'bold')
            ]
        }
    ])
    return st.table(styled)
    
    st.dataframe(styled, use_container_width=True)


#====================================================
#Funções geração de gráficos
#====================================================

def get_top_deliverys(df, tipo='rapido'):
    cols = ['City', 'Delivery_person_ID', 'Time_taken(min)']
    df_base = df[cols].copy()

    if tipo == 'rapido':
        agrupado = df_base.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].min().reset_index()
        ordenado = agrupado.sort_values(['City', 'Time_taken(min)'], ascending=[True, True])
    elif tipo == 'lento':
        agrupado = df_base.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].max().reset_index()
        ordenado = agrupado.sort_values(['City', 'Time_taken(min)'], ascending=[True, False])
    else:
        raise ValueError("Tipo deve ser 'rapido' ou 'lento'.")

    resultado = ordenado.groupby('City').head(10).reset_index(drop=True)
    return resultado


def top_delivery_rating(df):
    cols = ['Delivery_person_ID', 'Delivery_person_Ratings']
    df_media_av_entregadores = df[cols].groupby(by='Delivery_person_ID').mean().reset_index()
    df_media_av_entregadores = df_media_av_entregadores.sort_values(by='Delivery_person_Ratings', ascending=False).head(10)
    return df_media_av_entregadores


def rating_by_traffic(df):
    cols = ['Delivery_person_Ratings', 'Road_traffic_density']
    df_media = df[cols].groupby(by='Road_traffic_density').mean().reset_index()
    df_desvio = df[cols].groupby(by='Road_traffic_density').std().reset_index()
    df_merged = pd.merge(
        df_media,
        df_desvio,
        on='Road_traffic_density',
        suffixes=('_media', '_desvio')
    ).rename(columns={
        'Road_traffic_density': 'Traffic',
        'Delivery_person_Ratings_media': 'Average Mean',
        'Delivery_person_Ratings_desvio': 'STD'
    })

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_merged['Traffic'],
        y=df_merged['Average Mean'],
        marker=dict(color=df_merged['Average Mean'], colorscale='Blues'),
        error_y=dict(type='data', array=df_merged['STD'])
    ))

    fig.update_layout(
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font_color='white',
        xaxis_title='Trânsito',
        yaxis_title='Média de Avaliação'
    )
    return fig

def rating_by_weather(df):
    cols = ['Delivery_person_Ratings', 'Weatherconditions']
    df_grouped = df[cols].groupby('Weatherconditions').agg(['mean', 'std'])
    df_grouped.columns = ['Average Mean', 'STD']
    df_grouped = df_grouped.reset_index().rename(columns={'Weatherconditions': 'Conditions Weather'})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_grouped['Conditions Weather'],
        y=df_grouped['Average Mean'],
        marker=dict(color=df_grouped['Average Mean'], colorscale='Blues'),
        error_y=dict(type='data', array=df_grouped['STD'])
    ))

    fig.update_layout(
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font_color='white',
        xaxis_title='Clima',
        yaxis_title='Média de Avaliação'
    )
    return fig

#====================================================
#Barra Lateral
#====================================================
st.header("Marketplace - Delivery Insights", divider="gray")

image_path = os.path.join('images', 'logo_cury_company.png')
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
    ['conditions Cloudy\t', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default= ['conditions Cloudy\t', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy']
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

#====================================================
#Layout Dashboard
#====================================================


with st.container():
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        maior_idade = df.loc[:, 'Delivery_person_Age'].max()
        col1.metric('Oldest Age', str(maior_idade))
    with col2:
        menor_idade = df.loc[:, 'Delivery_person_Age'].min() 
        col2.metric('Youngest Age', str(menor_idade))
    with col3:
        melhor_condicao = df.loc[:, 'Vehicle_condition'].max()
        col3.metric('Best Vehicle Condition', str(melhor_condicao))
    with col4:
        pior_condicao = df.loc[:, 'Vehicle_condition'].min()
        col4.metric('Worst Vehicle Condition', str(pior_condicao))
with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Top 10 Delivery Person')
        df_media_av_entregadores = top_delivery_rating(df)
        styled_table(df_media_av_entregadores)
    with col2:
        st.markdown('Average rating per traffic conditions')
        fig_trafego = rating_by_traffic(df)
        st.plotly_chart(fig_trafego, use_container_width=True)
with st.container():
        st.markdown("""---""")
        st.markdown('Average rating by weather conditions')
        fig_clima = rating_by_weather(df)
        st.plotly_chart(fig_clima, use_container_width=True)

with st.container():
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Top 10 Fastest Delivery Persons by City')
        kpi_entregador_rapido = get_top_deliverys(df, tipo='rapido')
        styled_table(kpi_entregador_rapido)
    with col2:
        st.markdown('Top 10 Slowest Delivery Persons by City')
        kpi_entregador_lento = get_top_deliverys(df, tipo='lento')
        styled_table(kpi_entregador_lento)

