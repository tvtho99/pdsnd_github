import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_valid_input(prompt, valid_options):
    """
    Prompts the user for input and validates it against a list of valid options.

    Args:
        (str) prompt: The input prompt for the user.
        (list) valid_options: List of valid input options.

    Returns:
        (str): Validated user input.
    """
    while True:
        user_input = input(prompt)
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please choose from {', '.join(valid_options).capitalize()}.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by (only valid values below), or "all" to apply no month filter
        (str) day - name of the day of week to filter by (only valid values below), or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    # Valid input options
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']
    valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']

    # get user input for city (Chicago, New York City, Washington). HINT: Use a while loop to handle invalid inputs
    city = get_valid_input("Please enter city (Chicago, New York City, Washington): ", valid_cities)

    # get user input for month (all, january, february, ... , june)
    month = get_valid_input("Please enter month (Jan, Feb, ..., Jun or all): ", valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input("Please enter day of the week (Mon, Tue, ..., Sun or all): ", valid_days)

    print('-' * 40)
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
    # Load data from file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day, and hour from Start Time
    df['month'] = df['Start Time'].dt.month_name().str[:3].str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str[:3].str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Get input month
    if month != 'all':
        df = df[df['month'] == month]

    # Get input day
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0].capitalize()
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0].capitalize()
    print('Most Common Day of Week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def stations_and_trip_stats(df):
    """Displays most popular stations and trip."""

    print('\nCalculating The Most Popular Stations And Trip...\n')
    start_time = time.time()

    # display the most common start station
    common_start_station = df['Start Station'].mode()[0].capitalize()
    print('Most Common Start Station:', common_start_station)

    # display the most common end station
    common_end_station = df['End Station'].mode()[0].capitalize()
    print('Most Common End Station:', common_end_station)

    # display the most common trip from start to end
    df['Trip'] = "From \"" + df['Start Station'] + "\" To \"" + df['End Station'] + "\""
    most_common_trip = df['Trip'].mode()[0]
    print('Most Common Trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_travel_time(label, travel_time):
    """Displays the formatted travel time."""
    
    hours, remainder = divmod(travel_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f'{label}: {int(hours):02}:{int(minutes):02}:{int(seconds):02}')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total and mean travel times
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    # display formatted travel times
    display_travel_time('Total Travel Time', total_travel_time)
    display_travel_time('Mean Travel Time', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\n', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\n', gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(np.min(df['Birth Year']))
        most_recent_year = int(np.max(df['Birth Year']))
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest Year of Birth: {earliest_year}')
        print(f'Most Recent Year of Birth: {most_recent_year}')
        print(f'Most Common Year of Birth: {most_common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def display_data(df):
    """Displays raw data."""
    row_start = 0

    while True:
        # prompt user if they want to see raw data
        raw_data = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        if raw_data not in ['yes', 'no']:
            print("Please enter a valid response (yes or no).")
            continue
        
        if raw_data == 'no':
            break
        
        # prompt user for how many rows to display
        while True:
            try:
                row_count = int(input('\nHow many rows do you wanna see?\n'))
                if row_count <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")

        row_end = row_start + row_count

        # check if the requested rows exceed available data
        if row_end > len(df):
            row_end = len(df)
            print(f"The last available row is {row_end}. Displaying rows {row_start} to {row_end}:\n")
            print(df.iloc[row_start:row_end])
            print("\nNo more data to display.")
            break

        print(f"Displaying rows {row_start} to {row_end}:\n")
        print(df.iloc[row_start:row_end])

        row_start += row_count


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        stations_and_trip_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
