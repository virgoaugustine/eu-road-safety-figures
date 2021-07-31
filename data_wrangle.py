#imports
import requests
import pandas as pd
import matplotlib.pyplot as plt

def response_is_good(resp):
    '''
    This function accepts a response as input and checks it's status code and content-type header
    to determine it's a valid URL.
    It returns True if the URL leads to an existing page.
    '''
    content_type=resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type)

def remove_non_numeric_chars(string):
    '''This function accepts a string as input and returns and converts it to an integer with only numeric characters.'''
    return int(''.join(filter(str.isdigit, string)))

def get_facts_table(url):
    '''
    This function accepts a URL to the wiki page, extracts and processes the table 
    according to the given requirements and saves the results to a csv file 
    in the directory the script is run.
    '''

    # Rename the columns needed in the table so it's easier to read and work with.
    rename_columns = {'Area (thousands of km2)[24]': 'Area', 'Population in 2018[25]': 'Population', 
                  'GDP per capita in 2018[26]': 'GDP Per Capita', 
                  'Population density (inhabitants per km2) in 2017[27]': 'Population Density',
                  'Vehicle ownership (per thousand inhabitants) in 2016[28]': 'Vehicle Ownership',
                  'Total Road Deaths in 2018[30]':'Total Road Deaths',
                  'Road deaths per Million Inhabitants in 2018[30]':'Road Deaths per Million Inhabitants'}
    
    # Columns to return from the table after renaming
    columns_wanted = ['Country', 'Area', 'Population', 'GDP Per Capita', 'Population Density',
                  'Vehicle Ownership', 'Total Road Deaths', 'Road Deaths per Million Inhabitants']
    
    try:
        with requests.get(url) as response:
            if response_is_good(response): 
                facts_table = pd.read_html(url, header=0)[2].rename(columns = rename_columns)
                facts_table = facts_table[columns_wanted]
                
                #insert the year column after 'Country' and give it a default value of 2018.
                facts_table.insert(2, 'Year', '2018')

                #Correct cell in GDP Per Capita Column from '11,500+a' to '11500'
                facts_table['GDP Per Capita'] = facts_table['GDP Per Capita'].map(lambda x: remove_non_numeric_chars(x))

                # Correct cell in Population Column from '82.792,351' to '82792351'
                facts_table['Population'] = facts_table['Population'].map(lambda x: remove_non_numeric_chars(x))
                
                #Because the last row in the dataframe contains the overall total, we need to sort the dataframe without including that last row

                eu_total = facts_table.tail(1) #Save the last row 
                #Sort the table by 'Road Deaths per Million Inhabitants' column from highest to lowest.
                facts_table = facts_table.iloc[:-1, :].sort_values(by=['Road Deaths per Million Inhabitants'], ascending=False)
                #insert the last row back into the table
                facts_table = facts_table.append(eu_total)
                
                #Save the table to a csvfile
                filename = 'facts_and_figures_table.csv'
                facts_table.to_csv(filename, sep=',')
                
                print (f'File saved as {filename}')

                return facts_table

            else:
                return 'Please check the URL is valid.'
    except requests.exceptions.RequestException as e:
        return f'Error: {str(e)} while attempting to fetch data from {url}'
    
    except ValueError:
        return 'This page has no table(s).'

def visualize_data(facts_table, column_to_visualize='Road Deaths per Million Inhabitants'):
    '''
    This function accepts the table generated from get_facts_table() and returns a visualization of the data.
    It also accepts a second parameter (type string) of the column you want to visualize the data by. 
    Default is 'Road Deaths per Million Inhabitants'
    '''
    try:
        facts_table.plot.bar(x='Country', y=column_to_visualize, color='red')
        plt.title('Road deaths in EU Countries')
        plt.xlabel('Country')
        plt.ylabel(column_to_visualize)
        plt.savefig(f'{column_to_visualize}_chart.jpg',dpi=100,bbox_inches='tight')    
        print(f'Chart saved as: {column_to_visualize}_chart.jpg')
    except KeyError:
        print('Please make sure the column you have selected exists in the csv table.')

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Road_safety_in_Europe'

    ft = get_facts_table(url)
    visualize_data(ft)





