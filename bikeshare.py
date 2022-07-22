import time
import pandas as pd
import numpy as np
import datetime
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york_city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - number of the month to filter by[1 for January till 12 for December], or "all" to apply no month filter
        (int) day - number of the day of week to filter by[0 for Monday till 6 for Sunday], or "all" to apply no day filter

    Error Handling:
        ValueError: Value Error could be raised when user inputs any other character than an integer
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    bad_user_input = True
    city = " "
    month = " "
    day = " "
    while bad_user_input:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        try:
            user_input = input("We have data from 3 cities in the USA!.\nPlease choose the city you wish to view the stats for.\nInput 1 for Chicago, 2 for New York City and 3 for Washington\n:")
            bad_user_input = False
            if int(user_input) == 1:
                city = 'chicago'
            elif int(user_input) == 2:
                city = 'new_york_city'
            elif int(user_input) == 3:
                city = 'washington'
            else:
                bad_user_input = True
        except ValueError:
            print("Please enter the option as shown in the prompt")
            bad_user_input = True
            continue
    user_input_city = " ".join(half_word.capitalize() for half_word in city.split("_"))
    bad_user_input = True
    while bad_user_input:
        # get user input for month (all, january, february, ... , june)
        try:
            user_input = input("We have data for 6 months in 2017 from January to June\n. Please Input\n 1 for January\n 2 for February \n 3 for March\n 4 for April\n 5 for May\n 6 for June\n 13 for All Months\n:")
            bad_user_input = False
            if int(user_input) in [1,2,3,4,5,6]:
                month = int(user_input)
                #user_input_month = datetime_object = datetime.datetime.strptime(str(month), "%m")
                user_input_month = calendar.month_name[month]
            elif int(user_input) == 13:
                month = int(user_input)
                user_input_month = "All Months"
            else:
                bad_user_input = True
        except:
            print("Please enter the option as shown in the prompt")
            bad_user_input = True
            continue

    bad_user_input = True
    while bad_user_input:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        try:
            user_input = input("If you want to view data for a particular day of the week, \n. Please Input\n 0 for Monday\n 1 for Tuesday \n 2 for Wednesday\n 3 for Thursday\n 4 for Friday\n 5 for Saturday\n 6 for Sunday\n 8 for All Days of the Week\n:")
            bad_user_input = False
            if int(user_input) in [0,1,2,3,4,5,6]:
                day = int(user_input)
                user_input_day = calendar.day_name[day]
            elif int(user_input) == 8:
                day = int(user_input)
                user_input_day = "All Days of the Week"
            else:
                bad_user_input = True
        except:
            print("Please enter the option as shown in the prompt")
            bad_user_input = True
            continue
    print (f"Your Selection Is:\n City: {user_input_city}\n Month: {user_input_month}\n Day: {user_input_day}")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - number of the month to filter by[1 for January till 12 for December], or "all" to apply no month filter
        (int) day - number of the day of week to filter by[0 for Monday till 6 for Sunday], or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    Error Handling:
        None
    """
    file_name = CITY_DATA.get(city)
    df = pd.read_csv(file_name)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['End Time'] =  pd.to_datetime(df["End Time"])
    if month!=13:
        df = df[df["Start Time"].dt.month == month]
    if day!=8:
        df = df.loc[df["Start Time"].dt.weekday == day]
    #print(f"Data Frame for the Selection:\n {df.head()}")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        (datframe) df - Pandas Dataframe loaded from the selected csv file and
        applied with filters as selected by the user
    Returns:
        None
    Error Handling:
        None
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['common_month'] = df['Start Time'].dt.month
    most_common_month = calendar.month_name[df['common_month'].mode()[0]]
    print(f"The Most Common Month of Travel: {most_common_month}")
    # display the most common day of week
    df['common_day_of_week'] = df['Start Time'].dt.weekday
    most_common_day_of_week = calendar.day_name[df['common_day_of_week'].mode()[0]]
    print(f"The Most Common Day of Week of Travel: {most_common_day_of_week}")
    # display the most common start hour
    df['common_start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = datetime.datetime.strptime(str(df['common_start_hour'].mode()[0]), "%H")
    most_common_start_hour = most_common_start_hour.strftime("%I %p")
    print(f"The Most Common Start Hour of Travel: {most_common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        (datframe) df - Pandas Dataframe loaded from the selected csv file and
        applied with filters as selected by the user
    Returns:
        None
    Error Handling:
        None
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The Most Common Start Station of Travel: {most_common_start_station}")
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The Most Common End Station of Travel: {most_common_end_station}")
    # display most frequent combination of start station and end station trip
    most_common_start_end_Station = df.groupby(['Start Station','End Station']).size().idxmax()
    print(f"The Most Common Combination of Start and End Station of Travel: {most_common_start_end_Station}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        (datframe) df - Pandas Dataframe loaded from the selected csv file and
        applied with filters as selected by the user
    Returns:
        None
    Error Handling:
        None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    df['trip duration']=df['End Time']-df['Start Time']
    print(f"Total Travel Time: {df['trip duration'].sum()}")
    # display mean travel time
    print(f"Mean Travel Time: {df['trip duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        (datframe) df - Pandas Dataframe loaded from the selected csv file and
        applied with filters as selected by the user
    Returns:
        None
    Error Handling:
        None
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of User Types:")
    for user_type in user_types.index:
        print(f"{user_type}: {user_types[user_type]}")
    # Display counts of gender
    if "Gender" in df.columns:
        gender_types = df['Gender'].value_counts()
        print("\nCount of Genders:")
        for gender_type in gender_types.index:
            print(f"{gender_type}: {gender_types[gender_type]}")
    else:
        print("\nNo Gender Data Available!!!")
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print(f"Earliest Birth Year: {int(earliest_birth_year)}")
        recent_birth_year = df['Birth Year'].max()
        print(f"Most Recent Birth Year: {int(recent_birth_year)}")
        common_birth_year = df['Birth Year'].mode()[0]
        print(f"Most Common Birth Year: {int(common_birth_year)}")
    else:
        print("\nNo Birth Year Data Available!!!")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_data(df):
    """Displays trip data on bikeshare users 5 rows at a time.

    Args:
        (datframe) df - Pandas Dataframe loaded from the selected csv file and
        applied with filters as selected by the user
    Returns:
        None
    Error Handling:
        ValueError: Value Error could be raised when user inputs any other character than an integer
    """
    trip_data= input("Would you like to view Individual trip data?\n Please Input 1 for yes!\n: ")
    bad_user_input = True
    while bad_user_input:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        try:
            if int(trip_data):
                for row_count in range(0,len(df.index),5):
                    if row_count == 0:
                        print(df.iloc[:5])
                        continue_print = input("Would you like to view the next 5 rows?\n Please Input 1 for yes!\n: ")
                        if int(continue_print) == 1:
                            continue
                        else:
                            bad_user_input = False
                            break
                    elif row_count + 5 >=  len(df.index):
                        print(df.iloc[row_count:len(df.index)])
                        bad_user_input = False
                    else:
                        print(df.iloc[row_count:row_count+5])
                        continue_print = input("Would you like to view the next 5 rows?\n Please Input 1 for yes!\n: ")
                        if int(continue_print) == 1:
                            continue
                        else:
                            bad_user_input = False
                            break
        except ValueError:
            bad_user_input = False
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        trip_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
