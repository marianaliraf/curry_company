import pandas as pd
from datetime import datetime
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

class Utils:
    def __init__(self):
        pass

    def read_dataset(self, caminho):
        dataset_cury = pd.read_csv(caminho)
        return dataset_cury
    
    
    def clean_dataset(self, df):
        #Tratamento dos Dados
        df = df.loc[df['Delivery_person_Age'] != 'NaN ']
        
        df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)
        df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)
        
        
        df = df.loc[df['multiple_deliveries'] != 'NaN ']
        df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)
        
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
        
        #Removendo espaços em branco de strings
        columns = ['ID', 'Road_traffic_density', 'Type_of_order', 'Type_of_vehicle', 'City', 'Time_taken(min)', 'Festival']
        for col in columns:
          df[col] = df[col].str.strip()
          df = df[(df[col] != 'NaN') & (df[col] != 'NaN ')]
        
        #Limpando coluna Time Taken
        df.loc[:, 'Time_taken(min)'] = df['Time_taken(min)'].str.replace('(min) ', '', regex=False).astype(float)
        return df



    def render_table_with_aggrid(self, dataframe):
        gb = GridOptionsBuilder.from_dataframe(dataframe)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
        gridOptions = gb.build()
    
        AgGrid(
                dataframe,
                gridOptions=gridOptions,
                update_mode=GridUpdateMode.NO_UPDATE,
                theme='alpine',
                classes="ag-theme-alpine",  # <- ESSENCIAL!
                custom_css={
                    ".ag-theme-alpine": {
                        "height": "300px",
                        "width": "100%",
                    }
                },
                fit_columns_on_grid_load=True
            )

