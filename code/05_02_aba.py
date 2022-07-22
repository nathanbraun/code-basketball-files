from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

response = requests.get('http://www.remembertheaba.com/ABAStatistics/ABATop20.html')

print(response.text)

aba_soup = Soup(response.text)

# aba_soup is a nested tag, so call find_all on it

tables = aba_soup.find_all('table')

# find_all always returns a list, even if there's only one element, which is
# the case here
len(tables)

# get the aba table out of it
aba_table = tables[0]

# aba_table another nested tag, so call find_all again
rows = aba_table.find_all('tr')

# this is a header row
rows[1]

# data rows
first_data_row = rows[2]
first_data_row

# get columns from first_data_row
first_data_row.find_all('td')

# comprehension to get raw data out -- each x is simple tag
[str(x.string) for x in first_data_row.find_all('td')]

# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

# call function
list_of_parsed_rows = [parse_row(row) for row in rows[2:]]

# put it in a dataframe
df = DataFrame(list_of_parsed_rows)
df.head()

# now lets get headers
# could just do it manually
df.columns = [str(x.string).lower() for x in rows[1].find_all('th')]

str_cols = ['name', 'years']
float_cols = ['fg%', '3p%', 'ft%', 'ppg']
int_cols = [x for x in df.columns if not ((x in str_cols) or (x in float_cols))]

df[float_cols] = df[float_cols].astype(float)

# gives an error
# df[int_cols] = df[float_cols].astype(int)

# fix attempt 1 - commented out because it doesn't work
# df[int_cols] = pd.to_numeric(df[int_cols], errors='coerce')

# fix attempt 2 - call pd.numeric on one column at a time
for int_col in int_cols:
    df[int_col] = pd.to_numeric(df[int_col], errors='coerce')


# done
df.head()

