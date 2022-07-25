import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }

#Hadling mixed case user inputs
def validate_user_input(user_input, input_type):
    while True:
        input_entered=input(user_input).lower()
        try:
            if input_entered in ['chicago', 'new york city', 'washington'] and input_type == 'city':
                break
            elif input_entered in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 'month':
                break
            elif input_entered in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'] and input_type == 'day':
                break
            else:
                if input_type == 'city':
                    print("Wrong typing. Try again.")
                if input_type == 'month':
                    print("Wrong typing. Try again.")
                if input_type == 'day':
                    print("Wrong typing. Try again.")
        except ValueError:
            print ("Wrong input")
    return input_entered

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
    city = validate_user_input("Which city would you like to explore data Chicago, New York City or Washington?\n", 'city')

    # TO DO: get user input for month (all, january, february, ... , june)
    month = validate_user_input("Which month would you like to use as filter January, February, March, April, May, June or all?\n", 'month')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = validate_user_input("Which day would you like to use as filter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n", 'day')

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

# Load csv file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day and hour from Start Time column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month using if
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week using if
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month: ', most_common_month)

    # TO DO: display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('Most Common Day: ', most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_comm_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station is: ', most_comm_start_station)

    # TO DO: display most commonly used end station
    most_comm_end_station = df['End Station'].mode()[0]
    print('Most Common End Station is: ', most_comm_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # I used groupby and sort the results in descending order
    combination_station=df.groupby(['Start Station','End Station'])
    most_frequent_combination = combination_station.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station: ', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Types in Data are: ',df['User Type'].value_counts())

    # Gender and Birth Year are not present in Washington data, to display them only from New York City and Chicago
    if city == 'washington':
        print("Gender and birth year are not available for Washington")
    else:

    # TO DO: Display counts of gender
        print('Gender Type count: ', df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print('Earliest Birth Year is: ',earliest_year)

        most_recent_year = df['Birth Year'].max()
        print('Most Recent Birth Year is: ',most_recent_year)

        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Birth Year is: ',most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#show 5 rows of raw data user
def raw_data(df):
    row=0
    while True:
        option_view_raw_data = input("Are you interested to see raw data? Enter 'yes' or 'no'\n").lower()
        if option_view_raw_data == "yes":
            print(df.iloc[row : row + 5])
            row += 5
        elif option_view_raw_data == "no":
            break
        else:
            print("Wrong typing. Try again")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
