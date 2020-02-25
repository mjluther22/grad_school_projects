# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:04:09 2019

@author: mjlut
"""

""" Web Scraping at https://www.basketball-reference.com/leagues/NBA_2019_games.html"""
#%% Load some libraries
import sys
import os
import pandas as pd
import selenium
import time
from bs4 import BeautifulSoup
import random
from datetime import datetime
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LassoLarsCV
#%% try opening webpage
# adjust the path for Python to find the chrome driver
sys.path.append("C:/Users/mjlut/Software/chromedriver_win32")

chromedriverpath = "C:/Users/mjlut/Software/chromedriver_win32/chromedriver.exe"

from selenium import webdriver as webd

# launch the "drone" browser - commanded from Python
mydriver = webd.Chrome(executable_path=chromedriverpath)

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games.html")
#%%
def get_all_attributes_of_element(driver, element):
    xx = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    return(xx)
#get_all_attributes_of_element(mydriver, box_score_link[0])

#%%
box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

#%%
def my_scrape_boxscore(driver, urlpage):
    try:
        driver.get(urlpage)
        
        myteams = driver.find_elements_by_class_name('game_summary.current')[0]
        win_team = myteams.find_elements_by_class_name('winner')[0]
        win_tname = win_team.find_element_by_css_selector('a').text
        lose_team = myteams.find_elements_by_class_name('loser')[0]
        lose_tname = lose_team.find_element_by_css_selector('a').text
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        win_table = soup.select("#box-" + str(win_tname) +"-game-basic")
        win_df = pd.read_html(str(win_table), header = 1)
        win_df = win_df[0]
        win_df["Starters"]  
        win_df["Opposing_Team"] = lose_tname
        
        date_area = driver.find_element_by_class_name("scorebox_meta")
        date_time = date_area.find_element_by_css_selector('div').text
        game_time, date = date_time.split(',', 1)
        win_df["game_time"] = game_time
        win_df["date"] = date
        
        lose_table = soup.select("#box-" + str(lose_tname) +"-game-basic")
        lose_df = pd.read_html(str(lose_table), header = 1)
        lose_df = lose_df[0]
        lose_df["Opposing_Team"] = win_tname
        lose_df["game_time"] = game_time
        lose_df["date"] = date
        
        full_box_score = pd.concat([win_df, lose_df], axis = 0).reset_index(drop = True)
        full_box_score = full_box_score[full_box_score.Starters != "Reserves"]
        full_box_score = full_box_score[full_box_score.Starters != "Team Totals"]
        
        return(full_box_score)
    except Exception as e:
        print("element is not clickable")
        print(e)
        
#%%
boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
#%%October
fulldf_oct = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_oct.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/fulldf_oct.csv")
#%%November

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-november.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_nov = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_nov.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/fulldf_nov.csv")
#%%December
mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-december.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_dec = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_dec.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/fulldf_dec.csv")
#%%January

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-january.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_jan = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_jan.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/fulldf_jan.csv")

#%%February

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-february.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_feb = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_feb.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/fulldf_feb.csv")

#%%March

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-march.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_mar = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_mar.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/fulldf_mar.csv")

#%%
full_season_df = pd.concat([fulldf_oct, fulldf_nov, fulldf_dec, fulldf_jan, fulldf_feb, fulldf_mar],
                           axis = 0).reset_index(drop=True)
#%%
full_season_df.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_season_df.csv")
# =============================================================================
# #%% Read csv if program closes
# recovered_full_season_df = pd.read_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_season_df.csv").reset_index(drop = True)
# recovered_full_season_df.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/recovered_full_season_df.csv")
# recovered_full_season_df = recovered_full_season_df.reset_index(drop = True) 
# #resetting index didn't work when reading the df in.
# print(recovered_full_season_df.iloc[0,3]) #still says 4: will have to drop that column
# #drop column "Unnamed: 0"
# recovered_full_season_df = recovered_full_season_df.drop(["Unnamed: 0"], axis = 1)
# print(recovered_full_season_df.iloc[0,3]) #7. We're in business again. 
# full_season_df = recovered_full_season_df.copy()
# =============================================================================
#%% Remove rows with DNP
# =============================================================================
# full_season1 = full_season_df.copy()
# full_szn = full_season1[full_season1]
# full_szn.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_szn.csv")
# 
# =============================================================================
type(full_season_df.iloc[0,3]) #string
print(full_season_df.iloc[0,3]) #7

"""Because of the way this was created, every value in this dataframe is a string
Unfortunately, we will have to hardcode out any 'Did Not Play', 'Did Not Dress', etc.
Once that is done, we can then change the numbers to numbers
The things we need to remove are:
    Did Not Play
    Did Not Dress
    Not With Team"""
#%% Remove all rows containing the above listed strings
full_season1 = full_season_df.copy()
full_season1 = full_season1[full_season1.MP != "Did Not Play"]
full_season1 = full_season1[full_season1.MP != "Did Not Dress"]
full_season1 = full_season1[full_season1.MP != "Not With Team"]
full_season1.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_season1.csv")
#Looks good

#%% Convert numeric values to numbers so we can create calculated columns.
"""We have 19 columns that we need to convert, and fortunately they are all connected. 
Can we convert all columns in one swoop? Columns FG to +/-, or columns 3-21"""
full_szn = full_season1.copy()
full_szn.iloc[:,2:20] = full_szn.iloc[:,2:20].apply(pd.to_numeric)

print(full_szn.iloc[0,2]) #4.0
type(full_szn.iloc[0,2]) #float
print(full_szn.iloc[0,19]) #+9
type(full_szn.iloc[0,19]) #string - this is ok, we won't use this column anyways. 
#all set to move on with creating calculated columns

#%% Create column for fantasy points using DraftKings standard scoring
#Will be easier if I create columns for double-double and triple double first
def double_double(df):
    if df["PTS"] >= 10 and df["AST"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["TRB"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["TRB"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["TRB"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["TRB"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["BLK"] >= 10 and df["STL"] >= 10:
        return(1)
    else:
        return(0)
        
full_szn["dbl-dbl"] = full_szn.apply(double_double, axis = 1) 
full_szn.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_szn.csv")
#%% Triple double
def triple_double(df): 
    if df["PTS"] >= 10 and df["AST"] >= 10 and df["TRB"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["AST"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["AST"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["TRB"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["TRB"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["STL"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["TRB"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["TRB"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["STL"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["TRB"] >= 10 and df["STL"] >= 10 and df["BLK"] >= 10:
        return(1)
    else:
        return(0)
full_szn["trip-dbl"] = full_szn.apply(triple_double, axis = 1) 
full_szn.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_szn.csv")

#%%
def classic_scoring(df):
    fantasy_points = (0.5 * df["3P"] +
                      0.5 * df["3P"] +
                      1.25 * df["TRB"] +
                      1.5 * df["AST"] +
                      2 * df["BLK"] -
                      0.5 * df["TOV"] +
                      1.5 * df["dbl-dbl"] +
                      3 * df["trip-dbl"])
    return(fantasy_points)

full_szn["fantasy_points"] = full_szn.apply(classic_scoring, axis = 1)
full_szn.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_szn.csv")

#%%Try creating lags using set_index, unstack.shift, and stack back

"""First, I'll try creating each lag in a separate dataframe, and then appending it to full_szn"""
lags_attempt1 = full_szn.copy()
lags_attempt1.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/lags_attempt1.csv")

def convert_str_to_date(a_string):
    date = datetime.strptime(a_string, " %B %d, %Y") #there's an odd space in front of the month
    return(date)

lags_attempt1["date_formatted"] = lags_attempt1["date"].apply(lambda x: convert_str_to_date(x))
#check that this worked properly
print(lags_attempt1.iloc[0,27]) #2018-10-16 00:00:00
type(lags_attempt1.iloc[0,27]) #pandas._libs.tslibs.timestamps.Timestamp

#%%Now that I have date as an actual date, try set_index
lags_attempt1_grouped = lags_attempt1.groupby(["Starters"])

def lag_by_group(key, value_df, shift_by = 1):
    df = value_df.assign(group = key) # this pandas method returns a copy of the df, with group columns assigned the key value
    return(df.sort_values(by = ["date_formatted"], ascending = True)
    .set_index(["date_formatted"])
    .shift(shift_by)
        )
    
dflist = [lag_by_group(g, lags_attempt1_grouped.get_group(g)) for g in 
          lags_attempt1_grouped.groups.keys()]

new_lags_attempt1 = pd.concat(dflist, axis = 0).reset_index()
type(new_lags_attempt1) #dataframe
new_lags_attempt1.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/new_lags_attempt1.csv")

"""That worked. Now, we need to do that 4 more times to get 5 lags, group the original dataframe the same way, and then append the lags."""
#%%Lag 2
dflist2 = [lag_by_group(g, lags_attempt1_grouped.get_group(g), shift_by = 2) for g in 
          lags_attempt1_grouped.groups.keys()]

new_lags_attempt2 = pd.concat(dflist2, axis = 0).reset_index()
new_lags_attempt2.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/new_lags_attempt2.csv")

#%% Lag3
dflist3 = [lag_by_group(g, lags_attempt1_grouped.get_group(g), shift_by = 3) for g in 
          lags_attempt1_grouped.groups.keys()]

new_lags_attempt3 = pd.concat(dflist3, axis = 0).reset_index()
new_lags_attempt3.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/new_lags_attempt3.csv")

#%% Lag4
dflist4 = [lag_by_group(g, lags_attempt1_grouped.get_group(g), shift_by = 4) for g in 
          lags_attempt1_grouped.groups.keys()]

new_lags_attempt4 = pd.concat(dflist4, axis = 0).reset_index()
new_lags_attempt4.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/new_lags_attempt4.csv")

#%%Lag 5
dflist5 = [lag_by_group(g, lags_attempt1_grouped.get_group(g), shift_by = 5) for g in 
          lags_attempt1_grouped.groups.keys()]

new_lags_attempt5 = pd.concat(dflist5, axis = 0).reset_index()
new_lags_attempt5.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/new_lags_attempt5.csv")

#%% append these lags to the grouped dataframe. 
full_grouped_df = new_lags_attempt1.shift(-1)
full_grouped_df.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_grouped_df.csv")
#shifted the first lagged df up one since that was already grouped. Now append lags.

full_grouped_df["fantasy_pts_lag1"] = new_lags_attempt1["fantasy_points"]
full_grouped_df["fantasy_pts_lag2"] = new_lags_attempt2["fantasy_points"]
full_grouped_df["fantasy_pts_lag3"] = new_lags_attempt3["fantasy_points"]
full_grouped_df["fantasy_pts_lag4"] = new_lags_attempt4["fantasy_points"]
full_grouped_df["fantasy_pts_lag5"] = new_lags_attempt5["fantasy_points"]
#%%
"""Ok now that we have our lags, we have one more variable to try to create:
    the average fantasy points up until that game.
    
    For games played: maybe try some sort of counter. Start it at one, add one for each line, and 
    when the player name changes, reset to one
    
    We will also need to keep a running total of the sum of a players points. When games played
    equals 1, this needs to equal the points played for that game. Else, it needs to equal that
    games points plus the sum of points from the row above (sum of points is a different column)"""

#%% Games played 

games_counter = 0
counter_list = []

for i in range (0, len(full_grouped_df)):
    try:
        if full_grouped_df.loc[i, "Starters"] == full_grouped_df.loc[i-1, "Starters"]:
            games_counter +=1
            counter_list.append(games_counter)
        else: 
            games_counter = 1
            counter_list.append(games_counter)
    except KeyError: #because we were searching i-1, we got an error in the first row
        games_counter = 1
        counter_list.append(games_counter) 


full_grouped_df["games_played"] = counter_list

#%% Sum each players points

"""What do we need to do here? 
1) Sum the points
2) Calculate the average points
3) Shift the average down one row"""
        
df_for_pts_sum = full_grouped_df.copy()
points_sum = df_for_pts_sum.groupby("Starters")["fantasy_points"].cumsum()

full_grouped_df["sum_player_points"] = points_sum

#%% Calculate the average and shift the average down 1 row.

full_grouped_df["player_pts_avg"] = full_grouped_df["sum_player_points"]/full_grouped_df["games_played"]

full_grouped_df["player_pts_avg"] = full_grouped_df["player_pts_avg"].shift(1)

full_grouped_df.to_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_grouped_df.pkl")

#%%%

"""Now it's time to remove the columns we don't need, split into test and train datasets, and model

What variables do we want to keep?
1) Starters
2) Opposing_Team
3) fantasy_points
4) fantasy_pts_lag1
5) fantasy_pts_lag2
6) fantasy_pts_lag3
7) fantasy_pts_lag4
8) fantasy_pts_lag5
9) player_pts_avg

Since we have lags, we also know we are going to have some Nan values. We have plenty of data,
let's drop all rows with nan"""

#%% Create new df

goodvars_df = full_grouped_df.filter(["Starters", "Opposing_Team", "fantasy_points", "fantasy_pts_lag1",
                                     "fantasy_pts_lag2", "fantasy_pts_lag3", "fantasy_pts_lag4",
                                     "fantasy_pts_lag5", "player_pts_avg"], axis = 1)
goodvars_df.to_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/goodvars_df.pkl")
goodvars_df.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/goodvars_df.csv")
#%% drop rows with nan
goodvars1 = goodvars_df.copy()
goodvars1 = goodvars1.dropna(axis = 0).reset_index(drop = True)

goodvars1.to_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/goodvars1.pkl")
goodvars1.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/goodvars1.csv")

#%% Split into test and train
goodvars1 = pd.read_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/goodvars1.pkl")
train, test = train_test_split(goodvars1, test_size = .4, random_state = 1211)

train.to_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/train.pkl")
test.to_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/test.pkl")

train = pd.read_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/train.pkl")
test = pd.read_pickle("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/test.pkl")

"""Data visualization time"""
#%% Correlation matrix
corr = train.corr()
plt.figure(figsize = (5,5))
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True,
    annot = True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)

"""As expected, everything is highly correlated."""

#%% Histograms

train.hist()
        
"""All right skewed."""

#%% Scatterplots

plt.scatter(train["fantasy_pts_lag1"], train["fantasy_points"])
plt.xlabel("fantasy_pts_lag1")
plt.ylabel("fantasy_points")
plt.show()

plt.scatter(train["fantasy_pts_lag2"], train["fantasy_points"])
plt.xlabel("fantasy_pts_lag2")
plt.ylabel("fantasy_points")
plt.show()

plt.scatter(train["fantasy_pts_lag3"], train["fantasy_points"])
plt.xlabel("fantasy_pts_lag3")
plt.ylabel("fantasy_points")
plt.show()

plt.scatter(train["fantasy_pts_lag4"], train["fantasy_points"])
plt.xlabel("fantasy_pts_lag4")
plt.ylabel("fantasy_points")
plt.show()

plt.scatter(train["fantasy_pts_lag5"], train["fantasy_points"])
plt.xlabel("fantasy_pts_lag5")
plt.ylabel("fantasy_points")
plt.show()

plt.scatter(train["player_pts_avg"], train["fantasy_points"])
plt.xlabel("average_fantasy_points")
plt.ylabel("fantasy_points")
plt.show()

"""As expected, all pretty linear, all are highly correlated."""
#%% Split into x and y variables
train_x = train.copy()
train_x = train_x.drop("fantasy_points", axis =1)

train_y = train.copy()
train_y = train_y["fantasy_points"]

test_x = test.copy()
test_x = test_x.drop("fantasy_points", axis = 1)


test_y = test.copy()
test_y = test_y["fantasy_points"]

#%% Get dummy variables for Starters and Opposing_Team - train
x_player_dummies = pd.get_dummies(train_x["Starters"])
x_player_dummies
len(x_player_dummies)
len(train_x)

x_team_dummies = pd.get_dummies(train_x["Opposing_Team"])
len(x_team_dummies)

train_x1 = pd.concat([train_x, x_player_dummies, x_team_dummies], axis = 1)
real_train_x = train_x1.drop(["Starters", "Opposing_Team"], axis = 1)
real_train_x

#%% Get dummy variables for Starters and Opposing_Team - train
test_x_player_dummies = pd.get_dummies(test_x["Starters"])
test_x_player_dummies
len(test_x_player_dummies)
len(test_x)

test_x_team_dummies = pd.get_dummies(test_x["Opposing_Team"])
len(test_x_team_dummies)

test_x1 = pd.concat([test_x, test_x_player_dummies, test_x_team_dummies], axis = 1)
real_test_x = test_x1.drop(["Starters", "Opposing_Team"], axis = 1)

real_test_x.shape
real_train_x.shape

"""Because of our random test-train split, we don't have the same dummy variables in each.
How do we overcome this?"""

#%% Fix the dummy variable problem

#get the missing columns
missing_cols = set(real_train_x.columns) - set(real_test_x.columns)

#add a missing column in the test set with default equal to 0
for c in missing_cols:
    real_test_x[c] = 0
    
#ensure the order of column in the test set is the same as the order in the train set
real_test_x = real_test_x[real_train_x.columns]

#check
real_train_x.shape #(915031, 507)
real_test_x.shape #(6442, 507)
#%% Model 1: Linear model with all predictors
regression = LinearRegression()

lm1 = regression.fit(real_train_x, train_y)
print(lm1.coef_)

#%% How does linear model perform on train data?

lm1_train_predict = lm1.predict(real_train_x)
mean_absolute_error(train_y, lm1_train_predict) #3.98

#%% How does linear model perform on test data? 

lm1_test_predict = lm1.predict(real_test_x)
mean_absolute_error(test_y, lm1_test_predict) #4.12

#%% Model 2: Lasso model
lasso1 = LassoLarsCV(cv = 10, precompute = False).fit(real_train_x, train_y)
lasso1_predict = lasso1.predict(real_test_x)
mean_absolute_error(test_y, lasso1_predict) #4.14

#%% Model 3: Neural Net 
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

model = Sequential()
model.add(Dense(15, input_dim = 507, kernel_initializer = "normal", activation = "relu"))
model.add(Dense(1, activation = "linear"))
model.summary()

model.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history = model.fit(real_train_x, train_y, epochs = 100, batch_size=50,  
                    verbose=1, validation_split=0.2)

nn_predict1 = model.predict(real_test_x)
mean_absolute_error(test_y, nn_predict1) #4.51 - not great

nn_train_predict1 = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1) #3.7

"""This is actually slightly worse than our linear models. Let's tinker with the parameters 
of the neural network and see if we can improve"""

#%% Neural Network attempt 2:

nn_model2 = Sequential()
nn_model2.add(Dense(400, input_dim = 507, kernel_initializer = "normal", activation = "relu"))
nn_model2.add(Dense(200, activation = "relu"))
nn_model2.add(Dense(100, activation = "relu"))
nn_model2.add(Dense(50, activation = "relu"))
nn_model2.add(Dense(25, activation = "relu"))
nn_model2.add(Dense(12, activation = "relu"))
nn_model2.add(Dense(1, activation = "linear"))
nn_model2.summary()

nn_model2.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history2 = nn_model2.fit(real_train_x, train_y, epochs = 500, batch_size=50,  
                    verbose=1, validation_split=0.2)

nn_predict2 = nn_model2.predict(real_test_x)
mean_absolute_error(test_y, nn_predict2) #4.857 - got worse. I would assume overfitting

#how did this do on the train model? 
nn_train_predict2 = nn_model2.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict2) #1.27 - so as assumed, overfitting.

"""So how can we avoid overfitting?"""
#%%

from keras.layers import Dense
from keras.regularizers import l1

nn_model3 = Sequential()
nn_model3.add(Dense(400, input_dim = 507, kernel_initializer = "normal", activation = "relu", 
                    activity_regularizer = l1(.001)))
nn_model3.add(Dense(200, activation = "relu", activity_regularizer = l1(.001)))
nn_model3.add(Dense(100, activation = "relu", activity_regularizer = l1(.001)))
nn_model3.add(Dense(50, activation = "relu", activity_regularizer = l1(.001)))
nn_model3.add(Dense(25, activation = "relu", activity_regularizer = l1(.001)))
nn_model3.add(Dense(12, activation = "relu", activity_regularizer = l1(.001)))
nn_model3.add(Dense(1, activation = "linear", activity_regularizer = l1(.001)))
nn_model3.summary()

nn_model3.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history3 = nn_model3.fit(real_train_x, train_y, epochs = 500, batch_size=50,  
                    verbose=1, validation_split=0.2)

#test performance
nn_predict3 = nn_model3.predict(real_test_x)
mean_absolute_error(test_y, nn_predict3) #got worse

#train_performance
nn_train_predict3 = nn_model3.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict3) #1.25 - overfitting seemed to get worse. 

#%% Let's try with 1 hidden layer that is halfway between inputs and output

nn_model4 = Sequential()
nn_model4.add(Dense(250, input_dim = 507, kernel_initializer = "normal", activation = "relu"))
nn_model4.add(Dense(1, activation = "linear"))
nn_model4.summary()

nn_model4.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history4 = nn_model4.fit(real_train_x, train_y, epochs = 500, batch_size=50,  
                    verbose=1, validation_split=0.2)

#test performance
nn_predict4 = nn_model4.predict(real_test_x)
mean_absolute_error(test_y, nn_predict4)  #5.46 - worse again

#train_performance
nn_train_predict4 = nn_model4.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict4) #1.38

"""Ok, we keep failing to improve on the overfitting issue. Let's go back closer to the 
initial neural net, and try some regularlization off of that. Also try a different optimizer"""
#%% Try model 1 with all the different optimizers
model1a = Sequential()
model1a.add(Dense(15, input_dim = 507, kernel_initializer = "normal", activation = "relu"))
model1a.add(Dense(1, activation = "linear"))
model1a.summary()

model1a.compile(loss = "mse", optimizer = "sgd", metrics = ["mse", "mae"]) #generates nan.

history = model1a.fit(real_train_x, train_y, epochs = 100, batch_size=50,  
                    verbose=1, validation_split=0.2)

nn_predict1a = model1a.predict(real_test_x)
mean_absolute_error(test_y, nn_predict1a)

nn_train_predict1a = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1a)

"""sgd generates nan"""
#%%
model1a = Sequential()
model1a.add(Dense(15, input_dim = 507, kernel_initializer = "normal", activation = "relu"))
model1a.add(Dense(1, activation = "linear"))
model1a.summary()

model1a.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"]) #generates nan.

history = model1a.fit(real_train_x, train_y, epochs = 500, batch_size=50,  
                    verbose=1, validation_split=0.2)

nn_predict1a = model1a.predict(real_test_x)
mean_absolute_error(test_y, nn_predict1a)
#got worse - this is the same as the first model, but with more epochs

nn_train_predict1a = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1a)
#%% Model 1, but with regularlization using l1 = .01
model1_reg = Sequential()
model1_reg.add(Dense(15, input_dim = 507, kernel_initializer = "normal", activation = "relu",
                     activity_regularizer = l1(.01)))
model1_reg.add(Dense(1, activation = "linear", activity_regularizer = l1(.01)))
model1_reg.summary()

model1_reg.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history = model1_reg.fit(real_train_x, train_y, epochs = 100, batch_size=50,  
                    verbose=1, validation_split=0.2)

model1_reg_predict = model1_reg.predict(real_test_x)
mean_absolute_error(test_y, model1_reg_predict) #4.53 - almost identical - .02 worse than model1

nn_train_predict1 = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1)

#%% Model 1, but with dropout rate of .25

from keras.layers.core import Dropout

model1_reg = Sequential()
model1_reg.add(Dense(15, input_dim = 507, kernel_initializer = "normal", activation = "relu"))
model1_reg.add(Dropout(.25))
model1_reg.add(Dense(1, activation = "linear"))
model1_reg.summary()

model1_reg.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history = model1_reg.fit(real_train_x, train_y, epochs = 100, batch_size=50,  
                    verbose=1, validation_split=0.2)

model1_reg_predict = model1_reg.predict(real_test_x)
mean_absolute_error(test_y, model1_reg_predict) #4.30
# a slight improvement, but still not as good as linear

nn_train_predict1 = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1)

#%% Model 1 with l1 and dropout

model1_reg2 = Sequential()
model1_reg2.add(Dense(15, input_dim = 507, kernel_initializer = "normal", activation = "relu",
                      activity_regularizer = l1(0.01)))
model1_reg2.add(Dropout(.25))
model1_reg2.add(Dense(1, activation = "linear"))
model1_reg2.summary()

model1_reg2.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history = model1_reg2.fit(real_train_x, train_y, epochs = 100, batch_size=50,  
                    verbose=1, validation_split=0.2)

model1_reg2_predict = model1_reg2.predict(real_test_x)
mean_absolute_error(test_y, model1_reg2_predict) #4.24 
# another slight improvement, but still ~.1 worse than linear. 

nn_train_predict1 = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1)

#%% keep toying and changing parameters
model1_reg2 = Sequential()
model1_reg2.add(Dense(10, input_dim = 507, kernel_initializer = "normal", activation = "relu",
                      activity_regularizer = l1(0.01)))
model1_reg2.add(Dropout(.25))
model1_reg2.add(Dense(1, activation = "linear"))
model1_reg2.summary()

model1_reg2.compile(loss = "mse", optimizer = "adam", metrics = ["mse", "mae"])

history = model1_reg2.fit(real_train_x, train_y, epochs = 100, batch_size=50,  
                    verbose=1, validation_split=0.2)

model1_reg2_predict = model1_reg2.predict(real_test_x)
mean_absolute_error(test_y, model1_reg2_predict) #4.24 
# another slight improvement, but still ~.1 worse than linear. 

nn_train_predict1 = model.predict(real_train_x)
mean_absolute_error(train_y, nn_train_predict1)
# =============================================================================
# n = full_grouped_df.Starters.unique()
# n
# len(n) #506 unique players. 
# type(n)
# =============================================================================
#%%
# =============================================================================
# mydriver.get("https://www.basketball-reference.com/boxscores/201810170CHO.html")
# 
# #%%
# myteams = mydriver.find_elements_by_class_name('poptip')[0]
# win_team = myteams.find_elements_by_class_name('winner')[0]
# win_tname = win_team.find_element_by_css_selector('a').text
# win_tname
# lose_team = myteams.find_elements_by_class_name('loser')[0]
# lose_tname = lose_team.find_element_by_css_selector('a').text
# lose_tname
# """Within the box score table, the id = "box-MIL-game-basic.
# Can we identify it by id = box-tname-game-basic"""
# =============================================================================
#let's try printing it
#box_score = mydriver.find_element_by_id("box-" + str(win_tname) +"-game-basic")
#print(box_score)
#that worked. Let's try to extract this as a dataframe using beautiful soup.
# =============================================================================
# html = mydriver.page_source
# soup = BeautifulSoup(html, "html.parser")
# win_table = soup.select("#box-" + str(win_tname) +"-game-basic")
# win_df = pd.read_html(str(win_table), header = 1)
# type(win_df) #why is it a list instead of a df?
# win_df = win_df[0]
# win_df["Starters"] #this works, we are a dataframe now
# #let's append the other team as a column 
# win_df["Opposing_Team"] = lose_tname
# 
# #We're going to want to put the date on there too
# date_area = mydriver.find_element_by_class_name("scorebox_meta")
# date_time = date_area.find_element_by_css_selector('div').text
# date_time #'7:00 PM, October 17, 2018'
# type(date_time)
# date_time[0]
# game_time, date = date_time.split(',', 1)
# game_time #'7:00 PM'
# date #' October 17, 2018
# #append these  to the dataframe
# win_df["game_time"] = game_time
# win_df["date"] = date
# win_df
# 
# #losing df
# lose_table = soup.select("#box-" + str(lose_tname) +"-game-basic")
# lose_df = pd.read_html(str(lose_table), header = 1)
# lose_df = lose_df[0]
# lose_df["Opposing_Team"] = win_tname
# lose_df["game_time"] = game_time
# lose_df["date"] = date
# lose_df
# 
# #good. Now combine both into one df. 
# full_box_score = pd.concat([win_df, lose_df], axis = 0).reset_index(drop = True)
# full_box_score #looks good. Just need to remove rows that say "Reserves" and "Team Totals"
# full_box_score = full_box_score[full_box_score.Starters != "Reserves"]
# full_box_score = full_box_score[full_box_score.Starters != "Team Totals"]
# full_box_score
# #%%
# """Ok now that we have the code to get the full box score for one game, we need to do this from
# the main page, and then tell it to go back. """
# 
# """First, let's make sure we can do one whole run through: click into page, make the dataframe,
# and click back onto the main page"""
# back_to_main_page = mydriver.find_element_by_class_name("full")
# 
# #Open main page
# mydriver = webd.Chrome(executable_path=chromedriverpath)
# mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games.html")
# 
# stats_table = mydriver.find_element_by_class_name("stats_table")
# box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
# box_score_link.click() #worked once, and now I'm running into ElementClickInterceptedException error
# back_to_main_page.click() #works
# 
# all_games_df = pd.DataFrame()
# #doesitwork = pd.concat([all_games_df, full_box_score], axis = 0) #yes, this will work
# 
# """Put it all together"""
# 
# """I think the issue with this is that not every element is clickable. How do we write it so that if it's 
# not clickable, it moves to the next line?"""
# 
# from selenium.common.exceptions import WebDriverException 
# 
# for row in stats_table.find_elements_by_css_selector('tr'):
#     try:
#         box_score_link.click()
#         myteams = mydriver.find_elements_by_class_name('poptip')[0]
#         win_team = myteams.find_elements_by_class_name('winner')[0]
#         win_tname = win_team.find_element_by_css_selector('a').text
#         lose_team = myteams.find_elements_by_class_name('loser')[0]
#         lose_tname = lose_team.find_element_by_css_selector('a').text
#         html = mydriver.page_source
#         soup = BeautifulSoup(html, "html.parser")
#         win_table = soup.select("#box-" + str(win_tname) +"-game-basic")
#         win_df = pd.read_html(str(win_table), header = 1)
#         win_df = win_df[0]
#         win_df["Starters"]  
#         win_df["Opposing_Team"] = lose_tname
#         date_area = mydriver.find_element_by_class_name("scorebox_meta")
#         date_time = date_area.find_element_by_css_selector('div').text
#         game_time, date = date_time.split(',', 1)
#         win_df["game_time"] = game_time
#         win_df["date"] = date
#         lose_table = soup.select("#box-" + str(lose_tname) +"-game-basic")
#         lose_df = pd.read_html(str(lose_table), header = 1)
#         lose_df = lose_df[0]
#         lose_df["Opposing_Team"] = win_tname
#         lose_df["game_time"] = game_time
#         lose_df["date"] = date
#         full_box_score = pd.concat([win_df, lose_df], axis = 0).reset_index(drop = True)
#         full_box_score = full_box_score[full_box_score.Starters != "Reserves"]
#         full_box_score = full_box_score[full_box_score.Starters != "Team Totals"]
#         all_games_df = pd.concat([all_games_df, full_box_score], axis = 0).reset_index(drop = True)
#         box_score_link = mydriver.find_element_by_css_selector("td[data-stat = 'box_score_text']")
#         back_to_main_page.click()
#     except WebDriverException:
#         print("element is not clickable")
# 
# 
# #%% Now that we have the webpage open, we need to open each box score for each month
# 
# #Let's see if the box scores are identified by any type of column. 
# #tr is row
# #td is column 
# #tbody seems to be entire table
# #but table is also defined as: table class = "suppress_glossary sortable stats_table now_sortable
# #stats_table = mydriver.find_element_by_class_name("stats_table")
# for row in stats_table.find_elements_by_css_selector('tr'):
#     print(box_score_link.text)
# 
# """Ok, so we know that we can loop through row by row, and box_score_link.text gets us
# the correct column. So why is it getting mad at me when I try the function above?"""
# 
# """Let's try clicking on just the box score in the first row to make sure that element is clickable"""
# 
# 
#    #for cell in row.find_elements_by_class_name('center'):
#        #print(cell.text)
# #the above code works to print out "Box Score", except for every time it's a new table. This is good news!
# #we were right about what stats_table is. We also now know how to access the item we need to click.
# #cell.click would open. Let's just focus on one for now, and then go back to the loop.
# """A Better way """
# #box_score_link = mydriver.find_element_by_css_selector("td[data-stat = "box_score_text"])
# #%% Within each box score
# """The above code shows we know how to loop through the Box Scores. But before that can 
# be applied, we need to make sure we know how to get the info we need
# 
# One potential issue here is there are 4 separate tables, and we only need 2 of them.
# Unfortunately, they all seem to be class "stats_table". How can I handle this?
# 
# We know the header for each of these tables has the team initials there. We also know that
# at the top of each box score page, there is a box containing boxes for all of the scores of games
# played on that same day. The first one is that particular game. Grab the initials in that first box, and 
# only read the tables for those.
# 
# The larger box id is div_other_scores. The class for the scores is teams poptip (I would assume teams is
# the correct one"""
# 
# 
# 
# 
# 
# =============================================================================
