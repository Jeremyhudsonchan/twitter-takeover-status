import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

path='/content/mastodon2.json'
with open(path) as json_data:
   obj = json.load(json_data)
  #  print(obj)
   df_m = pd.DataFrame(obj['data']['platforms'][0]['statSet'], columns=['date','usersMonthly','usersTotal'])
   
df_m.info()

# convert date to datetype, sort and reset index by extracting ones from 2022
df_m['date'] = pd.to_datetime(df_m['date'])
df_m=df_m.sort_values(by='date')

mask=df_m['date']>'2021-12-31'
df_m=df_m.loc[mask].reset_index(drop=True)

df_m

plt.figure(figsize=(18,6))
plt.title("Mastodon user numbers")
plt.plot(df_m['date'],df_m['usersMonthly'],color='r',label='Monthly Active User')
plt.plot(df_m['date'],df_m['usersTotal'],color='b',label='Total User')
plt.legend()
plt.show()

Nov_interval = ('2022-10-22','2022-11-21')

# mask1=(df_m['date'] >= Apr_May_interval[0]) & (df_m['date'] <= Apr_May_interval[1])
mask1=(df_m['date'] >= Nov_interval[0]) & (df_m['date'] <= Nov_interval[1])
df1 = df_m.loc[mask1].reset_index(drop=True)
# df2 = df_m.loc[mask2].reset_index(drop=True)

df1['Diff'] = df1['usersTotal'].diff()
df1.at[0,'Diff']=0

df1.head()

plt.figure(figsize=(18,6))
plt.title('New infections October-November')
plt.plot(df1['date'],df1['Diff'],color='r')
for x, y in zip(df1['date'], df1['Diff']):
    plt.text(x=x, y=y, s=y,rotation=60)
plt.show()

t=np.arange(len(df1))
df1_t = pd.concat([df1, pd.DataFrame(t, columns=["t"])], axis=1)

df1_t.head()