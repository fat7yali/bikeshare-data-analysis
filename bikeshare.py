import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the city you want to analyze, type:(Chicago or New York City or Washington)\n').lower()
    while city not in CITY_DATA.keys():
        print('that\'s invalid input')
        city = input('Enter the city you want to analyze, type:(Chicago or New York City or Washington)\n').lower()

    # get user input for month (all, january, february, ... , june)

    month = input('To filter the data by a particular month, please type the month:(January, February, March, April, May, June, All(to apply no month filter))\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all' ]:
        print('that\'s invalid input')
        month = input('To filter the data by a particular month, please type the month:(January, February, March, April, May, June, All(to apply no month filter))\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Enter the day of week to filter by:(Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All(to apply no day filter))\n').lower()
    while day not in['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']:
        print('that\'s invalid input')
        day = input('Enter the day of week to filter by:(Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All(to apply no day filter))\n').lower()

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
         common_month = df['month'].mode()[0]
         print('\nMost common month:', common_month)

    # display the most common day of week
    if day == 'all':
        common_day = df['day_of_week'].mode()[0]
        print('\nMost common day of week: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nMost common start hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('\nMost common start station:', common_start)


    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nMost common end station:', common_end)


    # display most frequent combination of start station and end station trip
    df['Route'] = df["Start Station"] + "-" + df["End Station"]
    common_combination = df['Route'].mode()[0]
    print('\nMost frequent trip:', common_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total trip duration:', total_duration)


    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('mean trip duration:', mean_duration)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser Types:\n{}'.format(user_types))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nGenders:\n{}'.format(gender_count))

        common_birthyear = df['Birth Year'].mode()[0]
        print('\nMost common birth year:', common_birthyear)

        earlist_birthyear = min(df['Birth Year'])
        print('\nEarliest birth year:', earlist_birthyear)

        recent_birthyear = max(df['Birth Year'])
        print('\nMost recent birth year:', recent_birthyear)
    except KeyError:
        print('\nSorry there\'s no Gender or Birth Year data for Washington')


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    print('\nRaw data is available to check... \n')
    display_raw = input('To View the availbale raw data in chuncks of 5 rows type: Yes or No (to exit)\n').lower()
    while display_raw not in ('yes', 'no'):
        print('That\'s invalid input, please enter yes or no only')
        display_raw = input('To view the available raw data in chuncks of 5 rows type: Yes or No (to exit) \n').lower()
   # The second while loop is on the same level and doesn't belong to the first.
    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], index_col = 0 ,chunksize=5):
                print(chunk)
                display_raw = input('To View the availbale raw in chuncks of 5 rows type: Yes or no(to exit)\n').lower()
                if display_raw != 'yes':
                    print('Thank You')
                    break
            break

        except KeyboardInterrupt:
            print('Thank you.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
