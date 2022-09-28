import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'feburary', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input('Would you like to see data for Chicago, New York City, or Washington?\n')).lower()
        if city in cities:
                break
        else:
            print('Please input a valid city')
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Please choose one of the following months to analyze:\n -january\n -feburary\n -march\n -april\n -may\n -june\n -all(for no month filter)\n')).lower()
        if month in months:
            break
        else:
            print('Please input a valid month or enter "all" for no filter')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('Please choose a day of the week to analyze:\n -sunday\n -monday\n -tuesday\n -wednesday\n -thursday\n -friday\n -saturday\n -all(for no day filter)\n')).lower()
        if day in days:
                break
        else:
            print('Please input a valid day of the week or enter "all" for no filter by day')
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Popular Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most popular start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most popular end station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['common_combo'] = df['Start Station'] + ' to ' + df['End Station']
    print("The most frequent trip is from {}".format(df['common_combo'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is:', total_time, "seconds")


    # display mean travel time
    mean_time = round(df['Trip Duration'].mean(), 1)
    print('The mean travel time is:', mean_time, "seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("The count for each user type:\n", user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        print("The count of use by gender:\n", gender_count)
    else:
         print("'Gender' column not in dataframe")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_birth = int(df["Birth Year"].min())
        recent_birth = int(df["Birth Year"].max())
        common_birth = int(df["Birth Year"].mode()[0])
        print("The earliest year of birth is {}\nThe most recent year of birth is {}\nThe most common year of birth is {}"
           .format(earliest_birth, recent_birth, common_birth))
    else:
        print("'Birth Year' column not in dataframe")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_display(df):
    """Offers user ability to view raw data 5 lines at a time"""

    answers = ['yes','no']
    #Asks if user wants to view data
    while True:
        raw_data = input("Would you like to view 5 lines of trip data:\nPlease answer'yes' or'no'\n").lower()
        if raw_data in answers:
            break
        else:
            print("Please input 'yes' or 'no'")

    #Start location
    i = 0

    while True:
        if raw_data == 'no':
            break
        if raw_data == 'yes':
            #Shows five rows of raw data
            pd.set_option('display.max_columns',200)
            print(df[i:i+5])
            #Increments to next 5 rows
            i += 5
            #Ask if user would like to continue viewing
            cont = input("Would you like to view the next 5 lines of trip data?:\n Please answer 'Yes' or 'No'\n ").lower()

            if cont != 'yes':
                break

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
