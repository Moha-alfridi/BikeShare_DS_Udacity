import time
import pandas as pd
import numpy as np
import matplotlib as plt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    # City input, validated to get the right input
    city = input('Please enter a city from this list (chicago, new york city, washington): \n')
    city = city.lower()

    while city not in {'chicago', 'new york city', 'washington'}:
        try:
            city = input('Invalid input, Chose one (chicago, new york city, washington))\n')
            city = city.lower()
        except city in {'chicago', 'new york city', 'washington'}:
            break

    # Month input, validated to get the right input
    month = input('Please enter a month from the list (all, january, february, ... , june): \n')
    month = month.lower()

    while month.lower() not in {'all', 'january', 'february', 'march', 'april',
        'may', 'june', 'july', 'august', 'september',
        'october', 'november', 'december'}:
        try:
            month = input('Invalid input, please enter a months from the list (all, january, february, ... , june): \n')
            month = month.lower()
        except month.lower() in {'all', 'january', 'february', 'march', 'april',
        'may', 'june', 'july', 'august', 'september',
        'october', 'november', 'december'}:
            break

    # Day input, validated to get the right input
    day = input('Please enter a day from the list (all, monday, tuesday, ... sunday):\n')
    day = day.lower()

    while day.lower() not in {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}:

        try:
            day = input('Invalid input, please enter a day from the list (all, monday, tuesday, ... sunday):\n')
            day = day.lower()
        except day.lower() in {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_months = df['month'].value_counts().idxmax()
    print('The most common month is : ', common_months)

    # TO DO: display the most common day of week
    common_days = df['day_of_week'].value_counts().idxmax()
    print('The most common day is : ', common_days)

    # TO DO: display the most common start hour
    common_hour = df['hour'].value_counts().idxmax()
    print('The most common hour is : ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('Most common start station is : ' + common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('Most common end station is : ' + common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    common_station = df[['Start Station', 'End Station']].mode().iloc[0]
    print('Most common Start and End stations are : {}, {}'.format(common_station[0], common_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time is :', total_travel, '/ Minutes')

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Total travel time is :', mean_time, '/ Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    for i, user_count in enumerate(user_type):
        print('{}: {}'.format(user_type.index[i], user_count))

    # TO DO: Display counts of gender
    if city == 'chicago':
        gender_type = df['Gender'].value_counts()
        for i, gender_count in enumerate(gender_type):
            print('{}: {}'.format(gender_type.index[i], gender_count))
    elif city == 'new york city':
        gender_type = df['Gender'].value_counts()
        for i, gender_count in enumerate(gender_type):
            print('{}: {}'.format(gender_type.index[i], gender_count))
    else:
        print('\n*', city, '* doesn\'t have Gender or Birth year column.')
        print('\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        birth_year = df['Birth Year']
        earliest_birth = birth_year.min()
        print('The earliest birth year is : ', earliest_birth)

        recent_birth = birth_year.max()
        print('The recent birth year is : ', recent_birth)

        common_birth = birth_year.value_counts().idxmax()
        print('Most common birth year is: ', common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def empty_cell(df, city):
    """Displays statistics on bikeshare empty cells."""

    print('\nCalculating empty cells ...\n')
    start_time = time.time()

    gender_null = np.count_nonzero(df['Gender'].isnull())
    print('Number of empty cells in \'{}\' for Gender column are {}'.format(city, gender_null))
    birth_null = np.count_nonzero(df['Birth Year'].isnull())
    print('Number of empty cells in \'{}\' for Birth Years column are {}'.format(city, birth_null))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):

    start_data = 0
    num_data = 5
    raw_data = input('do you want to see raw data?\n')
    while raw_data.lower() != 'no':
        try:
            raw_data = df.iloc[start_data:num_data]
            print(raw_data)
            raw_data = input('\ndo you want to see raw data?\n')
            start_data += 5
            num_data += 5
        except raw_data.lower() == 'no':
            break



def main():
    while True:
        city, month, day = get_filters()
        print('You have chose to work with the '
              'City of: {}, Month of: {}, and Day of: {}'.format(city.title(), month.title(),day.title()))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        if city != 'washington':
            empty_cell(df, city)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart not in {'yes', 'no'}:
            try:
                restart = input('Invalid input, use yes or no')

            except restart in {'no'}:
                break
        if restart.lower() == 'no':
            break




if __name__ == "__main__":

    main()
