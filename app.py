import os
import re
import pickle
import streamlit as st
from dotenv import load_dotenv
import pathlib
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px


os.environ["TOKENIZERS_PARALLELISM"] = "false"
# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------

PATH = pathlib.Path(__file__).parent
REMOTE_DATA = 'us_jobs.csv'
DATA_PATH = PATH.joinpath("data-source").resolve()
OTHER_PATH = PATH.joinpath("other-datasets").resolve()


# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
# @st.cache_data
# def get_data():
#     # collect data frame of reviews and their sentiment
    
#     b2.set_bucket(os.environ['B2_BUCKETNAME'])
#     df_portals = b2.get_df(REMOTE_DATA)

#     return df_portals
        
# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
# b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
#         key_id=os.environ['B2_KEYID'], 
#         secret_key=os.environ['B2_APPKEY'])  

#kb = KeyBERT()
# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 1 : Pull data
# ------------------------------

st.set_page_config(page_title = "Debt Sustainability Analysis")

def on_text_area_change():
    st.session_state.page_text = st.session_state.my_text_area

st.write(
'''
# Title of DSA Project
''')

### Get Job_Portal DataFrame
#df_jobs = get_data()


st.write(

    '''
    ### This App is designed to be an interactive Sovereign Credit Risk Analysis Tool

    ## To simulate a credit-risk scenario, first choose a country,

    '''

)

df = pd.read_csv('/content/change in debt.csv',low_memory=False, sep=";", header=0)
df.rename(columns = {'Tahun':'Year'},inplace = True)
detail = df


economic_indicators = pd.read_csv('/content/economic-indicators.csv',low_memory=False, sep=";", header=0)

economic_indicators['Nominal Gross Public Debt'] = round(economic_indicators['Debt']/economic_indicators['GDP Current Price']*100,2)
economic_indicators['Public Debt (in percent of potential GDP)'] = round(economic_indicators['Debt']/economic_indicators['Potensial GDP']*100,2)
economic_indicators['Nominal GDP Growth (in percent)'] = round((economic_indicators['GDP Current Price']/economic_indicators['GDP Current Price (t-1)']-1)*100,2)
economic_indicators['Public Gross Financing Needs'] = round(((economic_indicators['Non Interest Expenditure']-economic_indicators['Non Interest Revenue'])+economic_indicators['Interest Payment']+economic_indicators['Amortization']-economic_indicators['Interest Receipt'])/economic_indicators['GDP Current Price']*100,2)
economic_indicators['Real GDP Growth (in percent)'] = round((economic_indicators['GDP Constant Price']/economic_indicators['GDP Constant Price (t-1)']-1)*100,2)
economic_indicators['Inflation (GDP deflator, in percent)'] = round((economic_indicators['GDP Deflator']/economic_indicators['GDP Deflator (t-1)']-1)*100,2)
economic_indicators['Effective Interest Rate (in percent)'] = round((economic_indicators['Interest Payment']/(economic_indicators['Debt  t-1']+economic_indicators['New Debt']))*100,2)


indic = economic_indicators[['Nominal Gross Public Debt','Public Gross Financing Needs','Public Debt (in percent of potential GDP)','Real GDP Growth (in percent)','Inflation (GDP deflator, in percent)','Nominal GDP Growth (in percent)','Effective Interest Rate (in percent)']]
index_ = ['2010-2018','2019','2020','2021','2022','2023','2024','2025','2026']
indic.index = index_
indicators = indic.transpose()
indicators.reset_index(inplace=True)
indicators = indicators.rename(columns = {'index':'Indicators'})

bondspread = pd.read_csv('/content/spread.csv',low_memory=False, sep=";", header=0)
bondratings = pd.read_csv('/content/bondratings.csv',low_memory=False, sep=";", header=0)

x = df['Year']

debt_creating_flows = go.Figure()
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Primary deficit'], name='Primary Deficit'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Real GDP growth'], name='Real GDP Growth'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Real interest rate'], name='Real Interest Rate'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Exchange rate depreciation'], name='Exchange Rate Depreciation'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Other debt-creating flows'], name='Other Debt-Creating Flows'))
debt_creating_flows.add_trace(go.Bar(x=x, y=df['Residual'], name='Residual'))
debt_creating_flows.add_trace(go.Scatter(x=x, y=df['Change in gross public sector debt'],
                    mode='lines+markers',
                    name='Change in gross public sector debt', line=dict(color='firebrick', width=4)))

debt_creating_flows.add_annotation(x=2022, y=9,
            text="Projections--->",showarrow=False)




debt_creating_flows.update_layout(barmode='relative',height=600, colorway=px.colors.qualitative.Vivid, 
                                  title=dict(text="Debt-Creating Flows (in Percent of GDP)",pad_t=0,pad_b=50,yanchor="top",
                                      y=1),
                                  legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                                  margin=dict(l=0,r=0,b=50,t=90,pad=4))

debt_creating_flows.update_xaxes(showgrid=False)

debt_creating_flows.add_vrect(x0="2021", x1="2027",fillcolor="#888",opacity=0.2, line_width=0)

st.plotly_chart(debt_creating_flows, use_container_width=True)
