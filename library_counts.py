"""
Data exploration using the City of Winnipeg's "Library People Counts" dataset.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set()

# Path to file
file_path = '../../Sample Data Sets/Library_People_Counts.csv'

# Read the file
counts = pd.read_csv(file_path)

# Remove the count IDs
counts = counts.drop(labels='ID', axis=1)

# Set the week as the index
counts = counts.set_index('Week End Date')

# Make the weeks into a time
counts.index = pd.to_datetime(counts.index)

# Go through the description column and separate out the library name only
counts['Library'] = [" ".join(desc.split()[:-4]) for desc in counts['Description']]

# Show the earliest recorded week for each library 
# The earliest counts start from Jan. 2009, but only in two libraries
print(counts.groupby('Library').apply(lambda x: x.index.min()).sort_values())

# Get the number of total counts per year in each library
by_library_and_year = counts.groupby(['Library', counts.index.year])['Count'].sum()
by_library_and_year = by_library_and_year.unstack(level=0).fillna(0)

# Alternatively, using pivot tables...
by_library_and_year = counts.pivot_table('Count', index=counts.index.year,
                                         columns='Library', aggfunc='sum').fillna(0)

# Get the total number of visitors to each library
by_library = by_library_and_year.sum().sort_values(ascending=True)

# Show the total number of visitors per library
plt.figure()
by_library.plot(kind='barh')
plt.gca().set_xlabel('Total visitors (millions)')
plt.gca().set_ylabel('Library')
plt.gca().set_title('Total Library Visitors')
plt.gca().set_xticks([0, 2000000, 4000000, 6000000, 8000000])
plt.gca().set_xticklabels([0, 2, 4, 6, 8])

# Group counts by year
by_year = counts.groupby(counts.index.year)['Count'].sum()

# Alternatively...
by_year = by_library_and_year.sum(axis=1)

# Show the total visitors per year
plt.figure()
by_year.plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Visitors (millions)')
plt.gca().set_title('Total Library Visitors')
plt.gca().set_yticks([0, 500000, 1000000, 1500000, 2000000, 2500000])
plt.gca().set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])

# Show the number of visitors per year for select libraries
plt.figure()
by_library_and_year[['St. Boniface', 'St. Vital']].plot(kind='bar')
plt.gca().set_ylim([0, 130000])
plt.gca().legend(loc='best')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Visitors')
plt.gca().set_title('Yearly Visitors for Selected Libraries')

# Get the number of visitors per month in each library
by_library_and_month = counts.pivot_table('Count', index=counts.index.month,
                                          columns='Library', aggfunc='sum').fillna(0)

# Group total visits by month
by_month = by_library_and_month.sum(axis=1)

# Show the total visitors per month
plt.figure()
by_month.plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Visitors (millions)')
plt.gca().set_title('Total Monthly Library Visitors')
plt.gca().set_yticks([0, 500000, 1000000, 1500000, 2000000, 2500000])
plt.gca().set_yticklabels([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])

# Show the number of visitors each month for select libraries
plt.figure()
by_library_and_month[['St. Boniface', 'Cornish']].plot(kind='bar')
plt.gca().set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.gca().set_ylim([0, 115000])
plt.gca().legend(loc='best')
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Visitors')
plt.gca().set_title('Monthly Visitors for Selected Libraries')

# Get total weekly visits over time
weekly_visits = counts['Count'].resample('W', kind='period').sum()

# Show total weekly visits for 2015
plt.figure()
weekly_visits['2015'].plot()
plt.gca().set_xlabel('Date')
plt.gca().set_ylabel('Visits')
plt.gca().set_title('Total Weekly Visitors in 2015')

# Get a new table with all counts for a given library in a week merged into one row
counts = counts.groupby([counts.index, 'Library'])
counts = counts.agg({'Count':'sum', 'Days Open':'max'}).reset_index('Library')

# Get the number of open days per year for each library
days_open = counts.pivot_table('Days Open', index=counts.index.year,
                                            columns='Library', aggfunc='sum').fillna(0)

# Compare the number of open days per year for St. Boniface and Millennium libraries
plt.figure()
days_open.loc[2010:2021][['Millennium', 'St. Boniface']].plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Number of days open')
plt.gca().set_title('Total Days Open Per Year')
plt.gca().set_ylim([0, 450])
plt.gca().legend(loc='best')

# Get the average number of visitors per open day in each library
visits_per_day = by_library_and_year/days_open

# Show the average number of visitors per day for St. Boniface and Millennium libraries
plt.figure()
visits_per_day[['Millennium', 'St. Boniface']].plot(kind='bar')
plt.gca().set_xlabel('Year')
plt.gca().set_ylabel('Average visitors per day')
plt.gca().set_title('Average Number of Visitors Per Day')
plt.gca().legend(loc='best')

plt.show()