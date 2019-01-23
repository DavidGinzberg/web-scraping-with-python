'''
community-groups.py example script to scrape tables
from wilmington community groups page
url: https://www.wilmingtonde.gov/government/city-offices/constituent-services/civic-and-neighborhood-organizations
'''

import requests
from bs4 import BeautifulSoup

target_url= "https://www.wilmingtonde.gov/government/city-offices/constituent-services/civic-and-neighborhood-organizations"

response = requests.get(target_url)
if response.status_code is not 200:
    print("Response code was not 200. Exiting")
    exit(response.status_code)

webpage_soup = BeautifulSoup(response.content, "html.parser")

tables = webpage_soup('table')



def list_table_headers(table_list):
    headers = list()
    for table in table_list:
        header = table.find("thead")
        if header is not None:  #Tables without headers cause problems without this check
            headers.append(header.get_text(strip=True))
    return headers

print("found tables with the following headers:")

for th in list_table_headers(tables):
    print(th)

def get_header_from_table(table):
    header = table.find("thead")
    if header is not None:
        return header.get_text(strip=True)
    else:
        return "<No table header>"

# for table in tables:
#     print(f"Table of type: {type(table)}")
#     for row in table.find_all('tr'):
#         print(f"Row of type: {type(row)}")

def list_of_fields_from_rows(row_list):
    field_list = list()
    for row in row_list:
        cells = row.find_all('td')
        #This assumes a 2-colunn table. Really only designed for the page we're working on
        if len(cells) is 2:
            field_list.append( 
                ( cells[0].get_text(), cells[1].get_text() ) 
            )
    return field_list

def build_table_dicts(table_list):
    table_dicts = list()
    for table in table_list:
        t_dict = dict()
        #From each table we want the header and all the fields (and their values)
        t_dict["title"] = get_header_from_table(table)
        #Add the fields to the dictionary
        t_dict["fields"] = list_of_fields_from_rows(table)
        #Add the dictionary of the current table to the list
        table_dicts.append(t_dict)

