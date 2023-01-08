import requests
from bs4 import BeautifulSoup
import pandas
import numpy
import translators

CHAMPIONS_LEAGUE_URL = 'https://www.zerozero.pt/competicao_stats.php?v=jt1&tp=t&id_competicao=27&esp=0'
WORLD_CUP_URL = 'https://www.zerozero.pt/competicao_stats.php?v=jt1&tp=t&id_competicao=30&esp=0'
PREMIER_LEAGUE_URL = 'https://www.zerozero.pt/competicao_stats.php?v=jt1&tp=t&id_competicao=4&esp=0'

df = pandas.DataFrame()
countries_list = []

response = requests.get(PREMIER_LEAGUE_URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")


for tag in soup.find_all(name='table', class_='zztable stats'):
    #  Where tag name is tr, it means this is a table row
    for row in tag.find_all(name='tr'):

        #  Where tag name is th, it means this is the header row of the table. th stands for Table Header
        header_row_values_list = []
        for header_row in row.find_all(name='th'):
            header_row_values_list.append(header_row.text)

        # We need create a dict with None values, so the dataframe is not empty
        # The fact the df is not empty (after the first iteration) comes in handy to avoid reassigning the header_dict
        # to the df variable, which would empty the df again, effectively erasing the lines that have been added
        # up until that point (lines added by iterations of the blocks after this one)
        header_dict = {item: None for item in header_row_values_list}
        if df.empty:
            df = pandas.DataFrame(header_dict, index=[0])  # append column names and None values if df is empty

        # Where tag name is td, it means this is a data row of the table. td stands for Table Data
        each_row_list = []
        for data_row in row.find_all(name='td'):
            each_row_list.append(data_row.text)

            # This means the variable each_row_list has the same number of values as the number of column in df
            # Therefore, append those values to the df and refresh each_row_list, so it's ready for the next iteration
            if len(each_row_list) == len(df.columns):
                df.loc[len(df)] = each_row_list
                each_row_list = []

        # Getting name of every player's country based on the flag image
        for image_tag in row.find_all(name='img'):
            countries_list.append(image_tag['title'])


# This comes before creating the Country column because len(countries_list) == x and len(df) == (x + 1)
# we delete the row with None values before creating Country column so that len(countries_list) == len(df)
df = df.replace(to_replace='None', value=numpy.nan).dropna()

# Creating Country column
df['Country'] = countries_list

# Translating country names from portuguese to english
df['Country'] = df['Country'].apply(lambda input_country_name: translators.translate_text(input_country_name))

# Renaming columns
correct_column_names = ['Rank', 'Player', 'Appearances', 'Matches',
                        'Goals', 'Penalty Goals', 'Own Goals', 'Minutes per Goal', 'Country']
rename_columns_dict = {df.columns[i]: correct_column_names[i] for i in range(0, len(df.columns))}
df = df.rename(columns=rename_columns_dict)

# Adjusting Rank column
df = df.replace(to_replace='', value=numpy.nan).fillna(method='ffill')
df['Rank'] = df['Rank'].astype(int)

# Create .csv file
df.to_csv('output-csv-files/top_20_all_time_premier_league_goalscorers.csv', index=False)
