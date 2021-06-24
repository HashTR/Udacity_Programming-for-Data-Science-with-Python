import time
import pandas as pd

CITY_DATA = {'Chicago':'chicago.csv',
             'New York City':'new_york_city.csv',
             'Washington':'washington.csv' }
months=('January', 'February', 'March', 'April', 'May', 'June')
wd=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

def Period_Factorization(p):
    """
    Factorize period in terms of seconds into five main factors weeks, days, hours, minutes and seconds

    Args:
        (time) p - Period in terms of seconds
    Returns:
        (str) s - Joined string of a period from its time factors
    """
    sec={'Weeks':604800,'Days':86400,'Hours':3600,'Minutes':60,'Seconds':1}
    f=[]
    for fa in sec:
        if p//sec[fa]>=1:
            if fa==list(sec.keys())[-1]:
                f.append(str(round(p,2))+' '+fa[:len(fa)-(p<=1)])
            else:
                f.append(str(int(p//sec[fa]))+' '+fa[:len(fa)-(p//sec[fa]==1)])
                p=p%sec[fa]
    J=', '.join(f)
    s=J[::-1].replace(', '[::-1], ' and '[::-1],1)[::-1]
    return s

def inplst(s,maxv):
    """
    List a string of numbers joined by ',' and convert to integer values
    Args:
        (str) s - String of joined numbers with ','
        (int) maxv - the maximum number that list values couldnot be exceeds
    Returns:
        (list) m or False - Return a list of integer values or 'False' if it doesn't match
    """
    try:
        m=[int(i) for i in s.replace(" ", "").split(',')]
        m.sort()
        if m[0]==0 or m==list(range(1,maxv+1)):
            return [0]
        elif max(m)>maxv:
            return False
        else:
            return m
    except ValueError:
        return False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('-^-'*20)
    print('Which city would you like to filter by?')
    print("Choose number from the list below (for example type '1'  for Chicago)")
    i=0
    s=[]
    s.append('All Cities')
    print('---'*4)
    print(str(i)+': '+s[i])
    for city in CITY_DATA:
        i+=1
        s.append(city)
        print(str(i)+': '+s[i])
    print('---'*4)
    print("Note: you may choose two cities (for example type '1,3' for both Chicago and Washington)")

    while True:
        ch = input("Your choice is:")
        city=inplst(ch,len(CITY_DATA.keys()))
        if city:
            print("You've choosed: " +', '.join([s[c] for c in city]))
            if city==[0]: city=list(range(1,len(CITY_DATA.keys())+1))
            break
        else:
            print("Sorry, '"+ch+"' doesn't match! Try again!")
    # TO DO: get user input for month (all, january, february, ... , june)
    print('-^-'*20)
    print('Which month would you like to filter by?')
    print("Choose number from the list below (for example type '1'  for January)")

    print('---'*4)
    print(str(0)+': '+'All Months')
    i=0
    for month in months:
        i+=1
        print(str(i)+': '+month)
    print('---'*4)
    print("Note: you may choose two months or more (for example type '1,3' for both January and March)")

    while True:
        ch = input("Your choice is:")
        month=inplst(ch,len(months))
        if month:
            if month==[0]:
                print("You've choosed: All Months")
                month=list(range(1,len(months)+1))
            else:
                print("You've choosed: " +', '.join([months[m-1] for m in month]))
            break
        else:
            print("Sorry, '"+ch+"' doesn't match! Try again!")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('-^-'*20)
    print('Which day of week would you like to filter by?')
    print("Choose number from the list below (for example type '1'  for Monday)")

    print('---'*4)
    print(str(0)+': '+'All Week Days')
    i=0
    for day in wd:
        i+=1
        print(str(i)+': '+day)
    print('---'*4)
    print("Note: you may choose two days or more (for example type '1,3' for both Monday and Wednesday)")

    while True:
        ch = input("Your choice is:")
        day=inplst(ch,len(wd))
        if day:
            if day==[0]:
                print("You've choosed: All Week Days")
                day=list(range(1,len(wd)+1))
            else:
                print("You've choosed: " +', '.join([wd[d-1] for d in day]))
            day=[i-1 for i in day]
            break
        else:
            print("Sorry, '"+ch+"' doesn't match! Try again!")


    print('*'*40)
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
    # load data file and put into a dataframe
    pth=list(CITY_DATA.values())
    df = pd.read_csv(pth[city[0]-1])
    if len(city)>1:
        for c in city[1:len(city)]:
            df=df.append(pd.read_csv(pth[c-1]))


    # convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the 'Birth Year' column (which may contain Null values) from float64 to int32
    try:
        df['Birth Year'] = df['Birth Year'].astype('Int32')
    except:
        pass

    # extract month, day of week and hour from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    df = df[df['month'].isin(month)]

    # filter by day of week if applicable
    df = df[df['day_of_week'].isin(day)]
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if df['month'].unique().size>1:
        most_month = df['month'].mode()[0]
        print('Most Common Month:', months[most_month-1])

    # TO DO: display the most common day of week
    if df['day_of_week'].unique().size>1:
        most_day = df['day_of_week'].mode()[0]
        print('Most Common Day:', wd[most_day])

    # TO DO: display the most common start hour
    most_hour = df['hour'].mode()[0]
    print('Most Common Hour:', most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    print('Most Common Start Station:', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most Common End Station:', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station']+" to: "+df['End Station']
    Start_Station, End_Station=df['Trip'].value_counts().idxmax().split(' to: ')
    print('Most Common Used Trip ----> \tfrom: ', Start_Station, " to: ", End_Station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Period_Factorization(Total_Travel_Time))

    # TO DO: display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Period_Factorization(Mean_Travel_Time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)
    # TO DO: Display counts of gender


    try:
        gender = df['Gender'].value_counts()
        print('Gender:\n', gender)
    except:
        print('Gender:','No Gender data Available')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('Earliest Year:', Earliest_Year)
    except:
      print("Earliest Year: No Birth Year data available")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('Most Recent Year:', Most_Recent_Year)
    except:
      print("Most Recent Year: No Birth Year data available")

    try:
      Most_Common_Year = df['Birth Year'].mode()[0]       #value_counts().idxmax()
      print('Most Common Year:', Most_Common_Year)
    except:
      print("Most Common Year: No Birth Year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)

def raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """
    S = 0
    answer = input('\nWould you like to see 5 rows of raw data? Enter yes or no: ').lower()
    while True:
        # Check if response is yes, print the raw data and increment count by 5
        if answer in ['yes','y']:
            E=S+5
            if E>df.shape[0]:
                E=df.shape[0]
            print(df[S:E])
            S=E
        else:
            break
        answer = input('\nWould you like to see more 5 rows of raw data? Enter yes or no: ').lower()


def main():
    while True:
        df = load_data(*get_filters())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        r = input('\nWould you like to restart? Enter yes or no:\n').lower()
        if r not in ['yes', 'y']:
            break


if __name__ == "__main__":
	main()
