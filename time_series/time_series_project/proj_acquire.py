import pandas as pd


###################
##
## All of this functions are coming from a file that has been imported like so:
##
## ##### file = open('csv-path-here').readlins()
## ##### for index,line in enumerate(file):
##  ##### file[index] = line.replace('\n','')
##
###################

def grab_foods(file):
    foods = []
    for line in file:
        if line == "":
            break
        foods.append(line)
    foods = foods[1:]
    return foods


def remove_foods(file):
    file = file.copy()
    while True:
        if file.pop(0) == '':
            break

    file.pop(0) ## Removes the "Activites"
    file.pop(0) ## Removes "Column names"

    return file

def grab_activities(file):
    file = file.copy()
    file = remove_foods(file)
    activities = {}
    for string in file:
        ### This checks to see if we hit the next empty string signifying we've oved on to food logs
        if string == "":
            break
        x = string.split('"')
        activities[x[1]] = {'total_calories':x[3],
                            'steps':x[5],
                           'distance':x[7],
                           'floors':x[9],
                           'mins_sedentary':x[11],
                           'mins_active_light':x[13],
                           'mins_active_med':x[15],
                           'mins_active_high':x[17],
                           'activity_calories':x[19]
                           }

    return activities

def remove_activities(file):
    file = file.copy()
    file = remove_foods(file)
    while True:
        if file.pop(0) == '':
            break

    return file

def grab_food_logs(file):
    file = file.copy()
    file = remove_activities(file)
    food_logs = {}
    while True:

        # if file[1] == 'Meal,Food,Calories':
        #     file.pop(1)
        # if file[1] == 'Breakfast':
        #     file.pop(2)
        #     file.pop(1)
        # if file[1] == 'Lunch':
        #     file.pop(2)
        #     file.pop(1)

        food_log = file.pop(0).split()[2]

        ### Some of the foodlogs don't follow the uniform pattern.
        ### This if statement circumvents (and deletes) the irregular data
        ### May come back and patch this to record the irregular data

        if file.pop(0) != 'Daily Totals' :
            while file.pop(0) != '"Daily Totals"':
                    ""
        calories = file.pop(0).split('"')[-2]
        fat = file.pop(0).split('"')[-2]
        fiber = file.pop(0).split('"')[-2]
        carbs = file.pop(0).split('"')[-2]
        sodium = file.pop(0).split('"')[-2]
        protien = file.pop(0).split('"')[-2]
        water= file.pop(0).split('"')[-2]
        file.pop(0)

        food_logs[food_log] ={'calories' : calories,
                         'fat' : fat,
                         'fiber' : fiber,
                         'carbs': carbs,
                         'sodium' : sodium,
                         'protien' :protien,
                         'water' : water}
        if len(file) == 0:
            return food_logs


def foods_to_dataframe(foods):
    food_dict = {}
    foodz = foods.copy()[1:]
    for i in foodz:
        split_str = i.split('"')
        food_dict[split_str[1]] = {'calories':split_str[3]}

    return pd.DataFrame(food_dict).T

def activities_to_dataframe(activities):
    return pd.DataFrame(activities).T


def food_logs_to_dataframe(food_logs):
    return pd.DataFrame(food_logs).T


def csv_to_dataframes(csv_path=''):
    file = open(csv_path).readlines()
    for index,line in enumerate(file):
        file[index] = line.replace('\n','')

    food_logs = grab_food_logs(file)
    foods = grab_foods(file)
    activities = grab_activities(file)



    foods_df = foods_to_dataframe(foods)
    activities_df = activities_to_dataframe(activities)
    food_logs_df = food_logs_to_dataframe(food_logs)

    return [foods_df,activities_df,food_logs_df]


def acquire_fitbit(csv_folder= './csvs'):

    csvs = ['2018-04-26_through_2018-05-26.csv',  '2018-08-27_through_2018-09-26.csv',
    '2018-05-27_through_2018-06-26.csv',  '2018-09-27_through_2018-10-27.csv',
    '2018-06-27_through_2018-07-27.csv',  '2018-10-28_through-2018-11-27.csv',
    '2018-07-28_through_2018-08-26.csv',  '2018-11-28_through_2018-12-28.csv']

    if csv_folder[-1] != '/':
        csv_folder = csv_folder+'/'

    df_lists = []
    for i in csvs:
        df_lists.append(csv_to_dataframes(csv_folder+i))

    foods = []
    activ = []
    logs = []
    for i in df_lists:
        foods.append(i[0])
        activ.append(i[1])
        logs.append(i[2])

    f_df = pd.concat(foods)
    a_df = pd.concat(activ)
    l_df = pd.concat(logs)

    return [f_df,a_df,l_df]