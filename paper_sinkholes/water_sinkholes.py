import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.anova import AnovaRM

months_dict = {'ene':1, 'feb':2, 'mar':3, 'abr':4, 'may':5, 'jun':6, 'jul':7, 'ago':8, 'sep':9, 'oct':10, 'nov':11, 'dic':12}

df = pd.read_csv('DATOS_2009-2017.csv')

df = df[['years','month','sinkholes','level']]

df['month'].replace(months_dict, inplace=True)

df['date'] = pd.to_datetime(df[['years', 'month']].assign(DAY=1)).dt.strftime('%Y-%m')

df = df[df['level']!= '(en blanco)']

df = df[['date','sinkholes','level']]

df['level'] = pd.to_numeric(df['level'], downcast="float")

count_entries_month = df.groupby('date').count().to_dict()['level']

months_ts, total_sinkholes = list(count_entries_month.keys()), list(count_entries_month.values())



df_subset = df[df['level']>0]

count_entries_month = df_subset.groupby('date').count().to_dict()['level']

months_tsg, total_sinkholes_greater = list(count_entries_month.keys()), list(count_entries_month.values())

count_average_month = df.groupby('date')['level'].mean().to_dict()

months_am, average = list(count_average_month.keys()), list(count_average_month.values())

sem_data = df.groupby('date')['level'].sem().to_dict()

months_sem, sem = list(sem_data.keys()), list(sem_data.values())

fig, ax1 = plt.subplots(figsize=(15,10))
ax1.set_xlabel('Month')
ax1.set_ylabel('Sinkhole Number')

ax1.plot(months_ts,total_sinkholes,'r',label='total sinkholes')
ax1.plot(months_tsg,total_sinkholes_greater,'k',label='total')
ax1.set_ylim([0, 160])
ax1.tick_params(axis='y')
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx() 

ax2.set_ylabel('Average Water Level')
ax2.set_ylim([0, 12])
ax2.bar(months_am,average,label='total', alpha = 0.3,yerr = sem,error_kw=dict(elinewidth=1, ecolor='b'),capsize=5)
ax2.tick_params(axis='y')
fig.tight_layout()
plt.savefig('plot')

#print(AnovaRM(data=df, depvar='level', subject='sinkholes', within=['date']).fit())