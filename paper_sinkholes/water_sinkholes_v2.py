import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.anova import AnovaRM
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

df = pd.read_csv('Sinkhole.csv')

df = df[['mes','abra','NIVEL','C/agua','A/C/F']]

df = df.rename(columns={'mes':'month_year','abra':'sinkhole','NIVEL':'level','C/agua':'water','A/C/F':'open_close'})

df['month_year']=pd.to_datetime(df['month_year'], format='%d/%m/%Y')

df = df[df['open_close']!='ND']
df = df.dropna(subset=['open_close','month_year'])

df['year'] = pd.DatetimeIndex(df['month_year']).year

#----------------------------------------------------------------------------------------------
df['open_close'] = pd.to_numeric(df['open_close'], downcast="float")
sum_open_close_month = df.groupby('month_year')['open_close'].sum().to_dict()

lista = []

for key_value in sum_open_close_month.items():
    lista.append((str(key_value[0].year),key_value[1]))

years_data = pd.DataFrame(lista, columns=['year','count'])

mean_open_close_year = years_data.groupby('year')['count'].mean().to_dict()

mean_open_close_year_keys=[]
mean_open_close_year_values=[]
for key, value in mean_open_close_year.items():
    mean_open_close_year_keys.append(key)
    mean_open_close_year_values.append(value)

#---------------------------------------------------------------------------------------------

df['water'].replace({"cerrada":0,"CERRADA":0},inplace=True)

df['water'] = pd.to_numeric(df['water'], downcast="float")
sum_water_month = df.groupby('month_year')['water'].sum().to_dict()

lista = []

for key_value in sum_water_month.items():
    lista.append((str(key_value[0].year),key_value[1]))

years_data = pd.DataFrame(lista, columns=['year','count'])

mean_water_year = years_data.groupby('year')['count'].mean().to_dict()

mean_water_year_keys=[]
mean_water_year_values=[]
for key, value in mean_water_year.items():
    mean_water_year_keys.append(key)
    mean_water_year_values.append(value)

#---------------------------------------------------------------------------------------------
df['level'].replace({"cerrada":0,"CERRADA":0},inplace=True)

df['level'] = pd.to_numeric(df['level'], downcast="float")
sum_level_month = df.groupby('month_year')['level'].sum().to_dict()

lista = []

for key_value in sum_level_month.items():
    lista.append((str(key_value[0].year),key_value[1]))

years_data = pd.DataFrame(lista, columns=['year','count'])

mean_level_year = years_data.groupby('year')['count'].mean().to_dict()
sem_level_year = years_data.groupby('year')['count'].sem().to_dict()

# np.std(datos, ddof=1) / np.sqrt(len(datos))

sem_level_year_keys=[]
sem_level_year_values=[]
for key, value in sem_level_year.items():
    sem_level_year_keys.append(key)
    sem_level_year_values.append(value)


mean_level_year_keys=[]
mean_level_year_values=[]
for key, value in mean_level_year.items():
    mean_level_year_keys.append(key)
    mean_level_year_values.append(value)

#--------------------------------------------------------------------
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Bar(
        x=mean_level_year_keys,
        y=mean_level_year_values,
        name="Level",
        error_y=dict(type='data', array=sem_level_year_values)),
    secondary_y=False,
    )

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1., opacity=0.5)

fig.add_trace(
    go.Scatter(
        x=mean_water_year_keys,
        y=mean_water_year_values,
    name="Sinkholes with water"),
    secondary_y=True)

fig.add_trace(
    go.Scatter(
        x=mean_open_close_year_keys,
        y=mean_open_close_year_values,
    name="Opened sinkholes"),
    secondary_y=True)

# Set x-axis title
fig.update_xaxes(title_text="<b>Year<b>")

# Set y-axes titles
fig.update_yaxes(title_text="Average <b>Water Level</b> [<i>cm</i>]", secondary_y=False,range=[0,1000])
fig.update_yaxes(title_text="<b>Sinkhole number<b>", secondary_y=True,range=[0,160])

fig.update_layout(
    width=950,
    height=600,
    margin=dict(l=80, r=40, t=20, b=40),
    paper_bgcolor='rgb(255, 255, 255)',
)

fig.write_image("fig1.png")
