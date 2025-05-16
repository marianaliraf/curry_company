import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117 !important;
        }
        html, body, [class*="css"] {
            background-color: #0e1117 !important;
            color: #c7d5e0 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4, p {
            color: #ffffff !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #ffffff;
            background-color: #1a202c;
            border-radius: 0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2d3748;
            border-bottom: 3px solid #4299e1;
        }
        .stSidebar, .css-1d391kg, .sidebar .css-1d391kg {
            background-color: #1a202c !important;
            color: white !important;
        }
        .stSlider > div[data-baseweb="slider"] {
            padding: 8px;
            border-radius: 5px;
            border: 1.5px solid #ffffff !important;
        }
        .stSlider .css-1cpxqw2 {
            color: #2b6cb0 !important;
        }
        .stSlider .css-14xtw13, .stSlider .css-1aumxhk {
            color: #2b6cb0 !important;
        }


        .stMultiSelect > div {
            background-color: #1a202c !important;
           
        }
        .stMultiSelect div[data-baseweb="tag"] {
            background-color: #2b6cb0 !important;
            color: #ffffff !important;
            font-weight: 500;
            border-radius: 8px;
        }
        .stMultiSelect div[data-baseweb="tag"] span {
            color: #ffffff !important;
        }
        .stMultiSelect label,
        .stMultiSelect span,
        .stMultiSelect div[data-baseweb="select"] * {
            background-color: #1a202c !important;
            color: #ffffff !important;
        }
        .stPlotlyChart {
            background-color: #0e1117;
        }
        .stButton > button {
            background-color: #2b6cb0;
            color: white;
            font-weight: bold;
        }
        .stSlider label, .stSlider span {
            color: #e2e8f0 !important;
        }
        .js-plotly-plot .xtick > text,
        .js-plotly-plot .ytick > text,
        .js-plotly-plot .legend text {
            fill: #ffffff !important;
        }
        .js-plotly-plot .xaxis > .xtitle,
        .js-plotly-plot .yaxis > .ytitle {
            display: none !important;
        }
        .stSidebar p, .stSidebar span, .stSidebar label {
            color: #e2e8f0 !important;
        }

        /* Estilos personalizados adicionados */
        .main-title {
            font-size: 36px;
            font-weight: 700;
            color: #edf2f7;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: #edf2f7;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .section-subtitle {
            font-size: 18px;
            font-weight: 500;
            color: #cbd5e0;
            margin-bottom: 1rem;
        }
        .sidebar-title {
            font-size: 20px;
            font-weight: 600;
            color: #edf2f7;
        }
        .sidebar-subtitle {
            font-size: 13px;
            color: #a0aec0;
        }
        .sidebar-footer {
            font-size: 11px;
            color: #718096;
        }

        /* Tentativa alternativa para inner track */
        div[data-baseweb="slider"] div[aria-valuenow] > div:first-child {
            color: #FFFFFF !important;
        }

        /* Linha do slider preenchida (inner track) */
        div[data-baseweb="slider"] div[role='slider'] {
            background-color: #2b6cb0 !important;
            border: 2px solid #2b6cb0 !important;
        }

        /* Linha de fundo total do slider (background track) */
        div[data-baseweb="slider"] > div:first-child > div {
             background: linear-gradient(to right, #ffffff 0%, #2b6cb0 0%) !important;
        }

        /* Estilo final para tabelas HTML com classe styled-table */
       .ag-theme-alpine {
            --ag-background-color: #1a202c;
            --ag-header-background-color: #2d3748;
            --ag-odd-row-background-color: #1a202c;
            --ag-row-hover-color: #2a2e39;
            --ag-foreground-color: #cbd5e0;
            --ag-header-foreground-color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Letras brancas para métricas */
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
        
        /* Cartões de métricas com fundo e borda */
        div[data-testid="metric-container"] {
            background-color: #1a202c;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #fffff !important;
            color: #ffffff !important;
        }

        </style>
    """, unsafe_allow_html=True)
