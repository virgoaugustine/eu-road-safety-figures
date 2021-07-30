#imports
import requests
import pandas as pd

def response_is_good(resp):
    '''
    This function uses some checks to determine if a given URL is valid. 
    It returns True if the URL leads to an existing page.
    '''
    content_type=resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type)

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
                
                #Sort the table by 'Road Deaths per Million Inhabitants' column from highest to lowest.
                facts_table = facts_table.sort_values(by=['Road Deaths per Million Inhabitants'], ascending=False)
                
                #Save the table to a csvfile
                filename = 'facts_and_figures_table.csv'
                facts_table.to_csv(filename, sep=',')
                
                return f'File saved as {filename}'
               

            else:
                return 'Please check the URL is valid.'
    except requests.exceptions.RequestException as e:
        return f'Error: {str(e)} while attempting to fetch data from {url}'
    
    except ValueError:
        return 'This page has no table(s).'

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Road_safety_in_Europe'

    print(get_facts_table(url))




