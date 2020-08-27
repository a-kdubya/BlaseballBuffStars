#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
from pandas.io.json import json_normalize
df = pd.read_json(r'https://blaseball.com/database/allTeams')


# In[2]:


df2 = df.loc[df['fullName'] == 'Kansas City Breath Mints']
df2


# In[3]:


df3 = pd.DataFrame([y for x in df2['lineup'].values.tolist() for y in x])
df3['list'] = pd.DataFrame([y for x in df2['lineup'].values.tolist() for y in x])
df3['position'] = 'lineup'
df4 = pd.DataFrame([y for x in df2['rotation'].values.tolist() for y in x])
df4['list'] = pd.DataFrame([y for x in df2['rotation'].values.tolist() for y in x])
df4['position'] = 'rotation'

string = ",".join(df3['list'])
string2 = ",".join(df4['list'])
string3 = string + "," + string2
url = 'https://blaseball.com/database/players?ids=%s' % string3
url

team = pd.read_json(url)


# team

# In[4]:


df3 = df3[['list','position']]
df4 = df4[['list','position']]
Batters = pd.merge(team, df3,left_on='id',right_on='list')
Pitchers = pd.merge(team,df4,left_on='id',right_on='list')
players = Batters.append(Pitchers)


# In[5]:


batting = Batters[['id',
            'name',
            'tragicness',
            'thwackability',
            'moxie',
            'divinity',
            'musclitude',
            'patheticism',
            'martyrdom']]

pitching = Pitchers[['id',
            
            'name',
            'shakespearianism',
            'unthwackability',
            'coldness',
            'overpowerment',
            'ruthlessness']]

baserunning = Batters[['id',
                
                'name',
                'baseThirst',
                'continuation',
                'groundFriction',
                'indulgence',
                'laserlikeness']]

defense = players[['id',
            
            'name',
            'anticapitalism',
            'chasiness',
            'omniscience',
            'tenaciousness',
            'watchfulness']]


# In[6]:


import numpy as np
batting.dtypes
batting['batting stars'] = round(((10 * (np.power(1 -batting['tragicness'],0.01) * np.power(batting['thwackability'],0.35) *np.power(batting['moxie'],0.075) * np.power(batting['divinity'],0.35)* np.power(batting['musclitude'],0.075) * np.power(1 -batting['patheticism'],0.05) * np.power(batting['martyrdom'],0.02)))/2
)*2)/2


pitching['pitching stars'] = round(((10 * (np.power(pitching['shakespearianism'],0.1)* np.power(pitching['unthwackability'],0.5) * np.power(pitching['coldness'],0.025)* np.power(pitching['overpowerment'],0.15) * np.power(pitching['ruthlessness'],0.4)))/2)*2)/2

defense['defense stars'] = round(((10* (np.power(defense['omniscience'] * defense['tenaciousness'],0.2)*np.power(defense['watchfulness'] * defense['anticapitalism']* defense['chasiness'],0.1)))/2)*2)/2

baserunning['baserunning stars'] = round(((10* np.power(baserunning['laserlikeness'],0.5) * (np.power(baserunning['baseThirst']*baserunning['continuation']*baserunning['groundFriction']*baserunning['indulgence'],0.1)))/2)*2)/2


# In[8]:


BuffTotal = .15

batting[['thwackability2','moxie2','divinity2','musclitude2','martyrdom2']]= batting[['thwackability','moxie','divinity','musclitude','martyrdom']] +.20


pitching[['shakespearianism2',
            'unthwackability2',
            'coldness2',
            'overpowerment2',
            'ruthlessness2']] = pitching[['shakespearianism',
                                        'unthwackability',
                                        'coldness',
                                        'overpowerment',
                                        'ruthlessness']] + BuffTotal

baserunning[['baseThirst2',
                'continuation2',
                'groundFriction2',
                'indulgence2',
                'laserlikeness2']] = baserunning[['baseThirst',
                                                'continuation',
                                                'groundFriction',
                                                'indulgence',
                                                'laserlikeness']] + BuffTotal
defense[['anticapitalism2',
            'chasiness2',
            'omniscience2',
            'tenaciousness2',
            'watchfulness2']] = defense[['anticapitalism',
                                        'chasiness',
                                        'omniscience',
                                        'tenaciousness',
                                        'watchfulness']] + BuffTotal


# In[9]:


import numpy as np
batting.dtypes
batting['buffed batting stars'] = round(((10 * (np.power(1 -batting['tragicness'],0.01) * np.power(batting['thwackability2'],0.35) *np.power(batting['moxie2'],0.075) * np.power(batting['divinity2'],0.35)* np.power(batting['musclitude2'],0.075) * np.power(1 -batting['patheticism'],0.05) * np.power(batting['martyrdom2'],0.02)))/2
)*2)/2

pitching['buffed pitching stars'] = round(((10 * (np.power(pitching['shakespearianism2'],0.1)* np.power(pitching['unthwackability2'],0.5) * np.power(pitching['coldness2'],0.025)* np.power(pitching['overpowerment2'],0.15) * np.power(pitching['ruthlessness2'],0.4)))/2)*2)/2


defense['buffed defense stars'] = round(((10* (np.power(defense['omniscience2'] * defense['tenaciousness2'],0.2)*np.power(defense['watchfulness2'] * defense['anticapitalism2']* defense['chasiness2'],0.1)))/2)*2)/2

baserunning['buffed baserunning stars'] = round(((10* np.power(baserunning['laserlikeness2'],0.5) * (np.power(baserunning['baseThirst2']*baserunning['continuation2']*baserunning['groundFriction2']*baserunning['indulgence2'],0.1)))/2)*2)/2


# In[10]:


pitching = pitching.append(pitching.sum(numeric_only=True),ignore_index=True)
pitching[['name']] =pitching[['name']].fillna('Total')
pitching['variance'] = pitching['buffed pitching stars'] - pitching['pitching stars']
pitching[['name','pitching stars','buffed pitching stars','variance']]


# In[11]:


batting = batting.append(batting.sum(numeric_only=True),ignore_index=True)
batting[['name']] = batting[['name']].fillna('Total')
batting['variance'] = batting['buffed batting stars'] - batting['batting stars']
batting[['name','batting stars','buffed batting stars','variance']]


# In[12]:


defense = defense.append(defense.sum(numeric_only=True),ignore_index=True)
defense[['name']] = defense[['name']].fillna('Total')
defense['variance'] = defense['buffed defense stars'] - defense['defense stars']
defense[['name','defense stars','buffed defense stars','variance']]


# In[13]:


baserunning = baserunning.append(baserunning.sum(numeric_only=True),ignore_index=True)
baserunning[['name']] = baserunning[['name']].fillna('Total')
baserunning['variance'] = baserunning['buffed baserunning stars'] - baserunning['baserunning stars']
baserunning[['name','baserunning stars','buffed baserunning stars','variance']]

