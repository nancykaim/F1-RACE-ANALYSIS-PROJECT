import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sb
import matplotlib.colors as mcloro
pink_palette = ['#F7CAC9', '#F4A7B9', '#F08CB4', '#ED6290', '#E6386D']

#defining file paths 
file_paths = {
    'circuits' : 'f1racedata/circuits.csv',
    'constructor_results' : 'f1racedata/constructor_results.csv',
    'constructor_standings' : 'f1racedata/constructor_standings.csv',
    'constructors' : 'f1racedata/constructors.csv',
    'driver_standings' : 'f1racedata/driver_standings.csv',
    'drivers' : 'f1racedata/drivers.csv',
    'lap_times' : 'f1racedata/lap_times.csv',
    'pit_stops' : 'f1racedata/pit_stops.csv',
    'qualifying' : 'f1racedata/qualifying.csv',
    'races' : 'f1racedata/races.csv',
    'results' : 'f1racedata/results.csv',
    'seasons' : 'f1racedata/seasons.csv',
    'sprint_results' : 'f1racedata/sprint_results.csv',
    'status' : 'f1racedata/status.csv',
    'team' : 'f1racedata/team.csv',
}

#cleaned data files
cleaned_file = {
    'cl_driver' : 'clean_data/cl_driv.csv',
    'cl_quali' : 'clean_data/cl_quali.csv',
    'cl_result' : 'clean_data/cl_result.csv',
    'cl_race_4' : 'clean_data/cl_race_4.csv',
    'cl_result_4' : 'clean_data/cl_result_4.csv',
    'cl_quali_4' : 'clean_data/cl_quali_4.csv',
    'season23' : 'clean_data/season23.csv',
    'agewin' : 'clean_data/yearwin.csv',
    
}

#loading csv files into separate dataframes 
df_circuits = pd.read_csv(file_paths['circuits'])
df_contr_res = pd.read_csv(file_paths['constructor_results'])
df_constr_stand = pd.read_csv(file_paths['constructor_standings'])
df_constr = pd.read_csv(file_paths['constructors'])
df_driver_stand = pd.read_csv(file_paths['driver_standings'])
df_drivers = pd.read_csv(file_paths['drivers'])
df_lapt = pd.read_csv(file_paths['lap_times'])
df_pitstop = pd.read_csv(file_paths['pit_stops'])
df_quali = pd.read_csv(file_paths['qualifying'])
df_races = pd.read_csv(file_paths['races'])
df_seasons = pd.read_csv(file_paths['seasons'])
df_sprint = pd.read_csv(file_paths['sprint_results'])
df_status = pd.read_csv(file_paths['status'])
df_results = pd.read_csv(file_paths['results'])
df_team = pd.read_csv(file_paths['team'])
df_23 = pd.read_csv(cleaned_file['season23'])
quali_cl = pd.read_csv(cleaned_file['cl_quali'])
cl_result = pd.read_csv(cleaned_file['cl_result'])
m23 = pd.read_csv(cleaned_file['season23'])
performance_df = pd.read_csv(cleaned_file['agewin'])
#functions 
def time_to_seconds(time_str):
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
        elif len(parts) == 2:
            h, m, s = 0, int(parts[0]), float(parts[1])
        else:
            h, m, s = 0, 0, float(parts[0])
        return h * 3600 + m * 60 + s
    except ValueError:
        return 0

 

def calculate_age_by_year(dob,race_year):
    birth_year = int(dob[:4])
    age = race_year-birth_year
    return age



#cleaning data
df_drivers = df_drivers[df_drivers['number'] != r'\N']
df_drivers.reset_index(drop=True, inplace=True)


df_drivers.to_csv(cleaned_file['cl_driver'], index=False)

cl_driv = pd.read_csv(cleaned_file['cl_driver'])

df_quali['q1'] = df_quali['q1'].astype(str)
df_quali['q2'] = df_quali['q2'].astype(str)
df_quali['q3'] = df_quali['q3'].astype(str)

df_quali['q1'] = df_quali['q1'].apply(time_to_seconds)
df_quali['q2'] = df_quali['q2'].apply(time_to_seconds)
df_quali['q3'] = df_quali['q3'].apply(time_to_seconds)
df_quali.to_csv(cleaned_file['cl_quali'])

df_results['fastestLapTime'] = df_results['fastestLapTime'].astype(str)
df_results['fastestLapTime'] = df_results['fastestLapTime'].apply(time_to_seconds)
df_results.replace(r'\N',0,inplace=True)
df_results.to_csv(cleaned_file['cl_result']) 

# age vs wins vs totalpoints each year

drivdata = df_drivers[['driverId','dob','forename','surname','nationality']].copy()
drivdata['drivname'] = drivdata['forename'] + ' ' + drivdata['surname']
drivdata.drop(columns=['forename','surname'], inplace=True)

resultdata = cl_result[['raceId', 'driverId','positionOrder','points']]
racedata = pd.read_csv(file_paths['races'])
racedata = racedata[['raceId','year']]
merge_agewin = pd.merge(drivdata,resultdata, on='driverId')
merge_agewin = pd.merge(merge_agewin,racedata, on='raceId')
merge_agewin = merge_agewin.sort_values(by='year',ascending=True)

wins_df = merge_agewin[merge_agewin['positionOrder']==1].groupby(['driverId','year']).size().reset_index(name='wins')
points_df = merge_agewin.groupby(['driverId','year'])['points'].sum().reset_index(name='totalpoints')
season_points_df = points_df.groupby('year')['totalpoints'].sum().reset_index(name='total_points_season')
performance_df = pd.merge(wins_df,season_points_df,on=['driverId','year'], how='outer').fillna(0)
drivinfo = merge_agewin[['driverId','drivname',]].drop_duplicates()
performance_df = pd.merge(drivinfo, performance_df, on='driverId',how='left')
performance_df.to_csv(cleaned_file['agewin'])



#cleaning data for driver number = 4 

# data from the year driver 4 has been active -> 2020-2023
df_races = df_races[df_races['year'] >= 2020]
df_races.reset_index(drop=True, inplace=True)
df_races.to_csv(cleaned_file['cl_race_4'])
df_races.replace(r'\N',0,inplace=True)

# race only of driver 4 
cl_res = pd.read_csv(cleaned_file['cl_result'])
cl_res = cl_res[cl_res['driverId'] == 846]
cl_res.reset_index(drop=True, inplace=True)
cl_res.replace(r'\N',0,inplace=True)
cl_res.to_csv(cleaned_file['cl_result_4'])


df_quali.replace(r'\N', 0, inplace=True)
df_quali.to_csv(cleaned_file['cl_quali'])
cl_quali = pd.read_csv(cleaned_file['cl_quali'])
cl_quali = cl_quali[cl_quali['driverId'] == 846]
cl_quali.reset_index(drop=True, inplace=True)
cl_quali.to_csv(cleaned_file['cl_quali_4'])
quali_4 = pd.read_csv(cleaned_file['cl_quali_4']) 


#merging and filtering dataframes
race_4 = pd.read_csv(cleaned_file['cl_race_4']) 
result_4 = pd.read_csv(cleaned_file['cl_result_4'])
merge_df_4 = pd.merge(race_4, result_4, on = 'raceId')


# race season 2023
races = df_races[['year','name','raceId']]
race_23 = races [df_races['year'] == 2023] 
race_23 = race_23.reset_index(drop='True')

quali23 = quali_cl[quali_cl['raceId'].isin(race_23['raceId'])]
quali23 = quali23.rename(columns={'position':'polepos'})
quali23.drop(columns=['Unnamed: 0' , 'q1','q2','q3', 'constructorId','number', 'qualifyId'], inplace=True)

result_23 = df_results[['raceId', 'driverId', 'statusId','positionOrder','points']]
result_23 = result_23.reset_index(drop = True)
merge_23 = pd.merge(race_23, result_23, on='raceId', how='inner')
merge_23 = pd.merge(merge_23, cl_driv, on='driverId')
merge_23 = pd.merge(merge_23, df_status, on = 'statusId')
merge_23 = pd.merge(merge_23, df_team, on = 'driverId')
merge_23 = pd.merge(merge_23, quali23, on=['raceId','driverId'])
merge_23['name'] = merge_23['name'].str.replace('Grand Prix', 'GP')
merge_23['drivName'] = merge_23['forename'] + ' ' + merge_23['surname']
merge_23.drop(columns=['url','driverRef','forename','surname','Unnamed: 0'], inplace=True)
merge_23.to_csv(cleaned_file['season23'])



#                                              ‧₊˚🖇️✩ ₊˚🎧⊹♡˚ ANALYSIS ‧₊˚🖇️✩ ₊˚🎧⊹♡         




# 🎀 fastest laptime of driver number 4 on each circuit 🎀
df4_2021 = merge_df_4[merge_df_4['year'] == 2021]
avg_laptime = df4_2021.groupby('name')['fastestLapTime'].mean().sort_values()
plt.figure(figsize= (12,8))
avg_laptime.plot(kind = 'barh', color = 'red')
plt.title('Lando Norris : Fastest LapTime vs Circuit (2021)')
plt.xlabel('Lapt Time')
plt.ylabel('Circuit Name')
plt.grid(axis='x')
plt.show()

# 🎀 highest rank in each year 🎀
high_pos4 = merge_df_4.groupby('year').apply(lambda x: x.loc[x['positionOrder'].idxmin()])[['year', 'positionOrder', 'name']]
plt.plot(high_pos4['year'], high_pos4['positionOrder'], marker='o', linestyle = '-', color='b', label='Highest Positionn')
plt.title('Highest Position Achieved Each Year')
plt.xlabel('Year')
plt.ylabel('Position')
plt.xticks(high_pos4['year'])
plt.grid(True)
plt.gca().invert_yaxis()
plt.legend()

for i,row in high_pos4.iterrows():
    plt.text(row['year'], row['positionOrder'], row['name'], ha='right', va='bottom')

plt.tight_layout()
plt.show()

# 🎀 Fastest Lap on miami grand prix from 2021-2024 🎀
miamigp = merge_df_4[(merge_df_4['name'] == 'Miami Grand Prix')]
fast_lap = miamigp[['year','fastestLap']]
fast_lap.plot( kind= 'bar', x='year', y='fastestLap', color='green')
plt.title('Fastest Lap by Lando Norris each year in Miami GP')
plt.xlabel('Year')
plt.ylabel('Fastest Lap (number)')
plt.xticks(rotation = 45)

plt.tight_layout()
plt.show()

# 🎀 Points by each team in 2023 🎀
team_points = df_23.groupby('team_name')['points'].sum().reset_index()

plt.figure(figsize= (10,8))
sb.barplot(y='team_name', x='points' , data= team_points, palette='viridis')
plt.xlabel('Points')
plt.ylabel('Team')
plt.title('Points Performance of Teams')
plt.show()

# 🎀 points by each player in 2023 🎀
driv_points = df_23.groupby('drivName')['points'].sum().reset_index()
max_points = driv_points.groupby('drivName')['points'].max().reset_index()
sorted_points = max_points.sort_values(by='points', ascending=False)['drivName'].tolist()
pivot_df = driv_points.pivot_table(index='drivName', values='points', aggfunc='sum').loc[sorted_points]

plt.figure(figsize=(10,7))
sb.heatmap(pivot_df, annot=True, cmap=sb.color_palette(pink_palette), fmt='.1f', linewidths=.5)
plt.title('Points scored by each driver')
plt.xlabel('Drivers')
plt.ylabel('Points')
plt.show()

# 🎀 Performance of each driver per race in 2023 🎀
plt.figure(figsize=(10,5))

sb.lineplot(data=m23, x='name', y='points', hue='drivName')
plt.xlabel('Race')
plt.ylabel('Points')
plt.title('Performance of each driver per race in 2023')
plt.legend(title='Driver Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout() 
plt.xticks(rotation=45)
plt.show()

# 🎀 Race vs Quali in 2023 🎀
plt.figure(figsize=(12, 6))
sb.lineplot(data=m23, x='name', y='polepos', hue='drivName', marker='o')
sb.lineplot(data=m23, x='name', y='positionOrder', hue='drivName', marker='o', linestyle='dashed')
plt.xlabel('Race')
plt.ylabel('Position')
plt.title('Performance Trend of Drivers in Qualifying vs Final Race Position')
plt.legend(title='Driver Name', bbox_to_anchor=(1.02, 1), loc='upper left')  # Adjust bbox_to_anchor as needed
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.gca().invert_yaxis()
plt.show()

# 🎀 Driver with most front rows and max wins  in 2023 🎀
pol_pos_23 = m23[m23['polepos'] == 1].groupby('drivName')['polepos'].count()
most_pole23 = pol_pos_23.idxmax()
driver_data = m23[m23['drivName'] == most_pole23]
wins_from_pole23 = driver_data[driver_data['positionOrder']==1].shape[0]
print(f"Driver with most pole positions: {most_pole23}") # Max Verstappen
print(f"Number of wins from pole positions: {wins_from_pole23}") #19 

# 🎀 Driver with most Wins without pole pos in 2023 🎀
without_pole_win23 = m23[(m23['positionOrder'] == 1) & (m23['polepos'] != 1)]
num_win_nopole23 = without_pole_win23.groupby('drivName').size()
most_win_not_from_pole23 = num_win_nopole23.idxmax()
print(f"Driver with most wins from non-1st positions: {most_win_not_from_pole23}") # Max Verstappen
print(f"Number of wins from non-1st positions: {num_win_nopole23.max()}") #6


# 🎀 comparisons of points and position relationship of drivers 🎀
rel_data = m23[['points','drivName','positionOrder']]
sb.pairplot(data=rel_data, hue='drivName')
plt.show()


# # 🎀 year vs win/points trend 🎀

#points vs years 
target_year = 2022
driv_target = ['Lewis Hamilton','Max Verstappen','Charles Leclrec','Lando Norris','Fernando Alonso','Kimi Räikkönen','Sebastian Vettel']
target_df=performance_df[performance_df['year']==target_year]
drivpts = target_df.groupby('drivname')['totalpoints'].sum()

cm=plt.get_cmap('tab20')
colours = cm.colors[:20]

fig, ax=plt.subplots()
wedges , _ = ax.pie(drivpts, startangle=90, colors=colours)
ax.axis('equal')
ax.legend(wedges,drivpts.index,title='Drivers',loc='right',bbox_to_anchor=(1, 0.5))
plt.title(f"Total Points Distribution for {target_year}")
plt.show()

# density analysis  
agerel_df = performance_df[performance_df['drivname'].isin(driv_target)].reset_index()
sb.relplot(
    data=agerel_df,
    y='year',
    x='totalpoints',
    hue='drivname',
    style='drivname'
)

sb.kdeplot(
    data=agerel_df, 
    y='year', 
    x='totalpoints', 
    fill=True, 
    alpha=0.3, 
    levels=7)

plt.title('points per year density')
plt.ylim(2002,2030)
plt.xlim(0, agerel_df['totalpoints'].max())
plt.show()

# years vs wins 

target_df=performance_df[performance_df['year']==target_year]
drivwins = target_df.groupby('drivname')['wins'].sum()

cm=plt.get_cmap('tab20')
colours = cm.colors[:20]

fig, ax=plt.subplots()
wedges , _ = ax.pie(drivwins, startangle=90, colors=colours)
ax.axis('equal')
ax.legend(wedges,drivwins.index,title='Drivers',loc='right',bbox_to_anchor=(1, 0.5))
plt.title(f"Total Points Distribution for {target_year}")
plt.show()

# density analysis 
agerel_df = performance_df[performance_df['drivname'].isin(driv_target)].reset_index()
sb.relplot(
    data=agerel_df,
    y='year',
    x='wins',
    hue='drivname',
    style='drivname'
)

sb.kdeplot(
    data=agerel_df, 
    y='year', 
    x='wins', 
    fill=True, 
    alpha=0.3, 
    levels=7)

plt.title('wins per year density')
plt.ylim(2002,2030)
plt.xlim(-5, agerel_df['wins'].max())
plt.show()


