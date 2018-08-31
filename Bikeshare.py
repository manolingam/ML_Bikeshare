#Importing necessary packages
import pandas as pd
import numpy as np

#contains the csv file name
all_csv = {'chicago':'chicago.csv',
             'new york':'new_york_city.csv',
                'washington':'washington.csv'}

"""These are used for validating inputs"""
expected_months = ['January','February','March','April','May','June']
expected_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
option = ['Yes', 'No']
month_map = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June'}

def get_filters():
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    city = input("Which city would you like to see the data for? type in exactly as Chicago, New york or Washington.\n")
    if (city == 'Chicago') or (city == 'New york') or (city == 'Washington'):
        city = city.lower()
        month = input('\nDo you like to filter by month? Type in Yes or No.\n')
        if month == 'Yes' and month in option:
            month = input('\nWhich month do you like to filter by? type in exactly as January, February, March, April, May or June.\n')
            if month in expected_months:
                day = input('\nDo you like to filter by day? Type in Yes or No.\n')
                if day == 'Yes' and day in option:
                    day = input("\nWhich day you want to filter by? type in exactly as Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n")
                    if day in expected_days:
                        print("\nGot it..")
                        #calling the next function
                        load_data(city, month, day)
                    else:
                        print("\nOops! Please type in exactly as mentioned. Restart the program now!\n")
                elif day == 'No' and day in option:
                    day = 'No'
                    print("\nGot it..")
                    #calling the next function
                    load_data(city, month, day)
                else:
                    print('\nOops! Please type in exactly as mentioned. Restart the program now!\n')  
            else: 
                print('\nOops! Please type in exactly as mentioned. Restart the program now!\n')   
        elif month == 'No' and month in option: 
            month = 'No'
            day = input('\nDo you like to filter by day? Type in Yes or No.\n')
            if day == 'Yes' and day in option:
                day = input("\nWhich day you want to filter by? type in exactly as Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n")
                if day in expected_days:
                    print("\nGot it..")
                    #calling the next function
                    load_data(city, month, day)
                else:
                    print("\nOops! Please type in exactly as mentioned. Restart the program now!\n")
            elif day == 'No' and day in option:
                day = 'No'
                print("\nGot it..")
                #calling the next function
                load_data(city, month, day)
            else:
                print('\nOops! Please type in exactly as mentioned. Restart the program now!\n')   
        else:
            print('\nOops! Please type in exactly as mentioned. Restart the program now!\n') 
    else:
        print("\nOops! Please type in exactly as mentioned. Restart the program now!\n")
    
def load_data(city, month, day):

    """Loads data for the specified city and filters by month and day if applicable."""

    df = pd.read_csv(all_csv[city])
    #Droped unnecessary column
    df = df.drop('Unnamed: 0',axis=1) 
    #NaN value count
    na_count = df.isnull().sum().sum() 
    if na_count!=0:
        print('Found ' + str(na_count) + ' NaN Values..\nFixing and Analysing..\n')
        #Dropped NaN rows
        df = df.dropna(axis=0) 
    else:
        print('Analysing now..\n')
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'No':
        month = expected_months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'No':
        df = df[df['day_of_week'] == day.title()]
        
    #calling next function
    time_stats(df, month, day, city) 

def time_stats(df, month, day, city):

    """Displays statistics on the most frequent times of travel."""

    print('\n----Calculating The Most Frequent Times of Travel----\n')

    # display the most common month
    if month =='No':
        common_month = df['month'].mode()[0]
        print('   Common month: ' + str(month_map[common_month]))
    else:
        print("   --Month filter already applied as " + str(month_map[month]) + "--\n")    
    
    # display the most common day of week
    if day =='No':
        common_day = df['day_of_week'].mode()[0]
        print('   Common day: ' + str(common_day) + '\n')
    else:
        print("   --Day filter already applied as " + str(day) + "--\n")    


    # display the most common start hour
    start_hour = df['Start Time'].dt.hour.mode()[0]
    if start_hour>12:
        print('   Common Start Hour: ' + str(start_hour-12) + 'PM')
    else:
        print('   Common Start Hour: ' + str(start_hour) + 'AM')    

    #calling next function
    station_stats(df, city) 

def station_stats(df, city): 

    """Displays statistics on the most popular stations and trip."""

    print('\n----Calculating The Most Popular Stations and Trip----\n')

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('   Common Start Station: ' + common_start_station)


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('   Common End Station: ' + common_end_station)

    # display most frequent combination of start station and end station trip    
    frequent_trip_raw = '(' + df['Start Station'].astype(str) + ") to (" + df['End Station'].astype(str) + ')'
    frequent_trip = frequent_trip_raw.describe()['top']
    print("   Most frequent trip: "+frequent_trip)

    #calling next function
    trip_duration_stats(df, city) 

def trip_duration_stats(df, city):

    """Displays statistics on the total and average trip duration."""

    print('\n----Calculating Trip Duration----\n')

    # display total travel time
    df['duration'] = pd.to_datetime(df['End Time'])- pd.to_datetime(df['Start Time'])
    df['duration'] = pd.to_datetime(df['duration']).dt.hour * 60 * 60 +  pd.to_datetime(df['duration']).dt.minute * 60 + pd.to_datetime(df['duration']).dt.second
    duration = df['duration'].sum()
    print('   Total Duration: ' + str(duration) + 's')

    # display mean travel time
    mean = df['duration'].mean()
    print('   Mean Travel Time: ' + str(mean) + 's')

    #calling next function
    user_stats(df, city) 

def user_stats(df, city):

    """Displays statistics on bikeshare users."""

    print('\n----Calculating User Stats----\n')

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('   User Types....')
    for i in range(len(user_types)):
        print('   ' + str(user_types.index[i]) + ": " + str(user_types[i]))
    
    # Display counts of gender
    if city!='washington':
        gender = df['Gender'].value_counts()
        print('\n   Gender Count....')
        for i in range(len(gender)):
            print('   ' + str(gender.index[i]) + ": " + str(gender[i]))
    else:
        print("\n   --Gender data not available--\n")    

    # Display earliest, most recent, and most common year of birth
    if city!='washington':
        earliest = df['Birth Year'].min()
        print('\n   Earliest Birth Year: ' + str(earliest))
        recent = df['Birth Year'].max()
        print('   Recent Birth Year: ' + str(recent))
        common_year = df['Birth Year'].mode()[0]
        print('   Most Birth Common Year: ' + str(common_year) + '\n')
    else:
        print("   --Birth data not available--\n")    

"""There is no main function here! Instead every other functions are called from within 
    the respective functions itself. Calling the first function get_filters() below. Others
    are called one by one within each functions"""

get_filters()