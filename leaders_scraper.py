

import requests
from bs4 import BeautifulSoup
import re
from requests import Session
import json

def get_first_paragraph(wikipedia_url, session: Session) -> str:

   # Query the url and get its content
   req = session.get(wikipedia_url)
   soup = BeautifulSoup(req.content)
   
   name = list(soup.find('h1').text)
   
   # Create paragraph list and empty first_paragraph variable
   paragraphs = [tag for tag in soup.find_all("p")]
   first_paragraph = ''

    # Loop over the paragraphs list and returning the first paragraph that contains the name
   for paragraph in paragraphs:
    if name[0] in paragraph.text and len(paragraph.text) > 50:
        first_paragraph = paragraph.text
        break
    # remove '\n' which comes at the end of some paragraphs
   first_paragraph = re.sub(r'\n', '', first_paragraph) 
    # remove [] and their content, which are usualy links to footnotes
   first_paragraph = re.sub(r'\[.*?\]', '', first_paragraph)
    # remove \xa0 from en sites
   first_paragraph = re.sub(r'[\xa0]', '', first_paragraph)

   return first_paragraph




def get_leaders() -> dict:
    
    leaders_per_country = {}

    root_url = 'https://country-leaders.onrender.com/'
    cookie_url = '/cookie'
    countries_url = '/countries'
    leaders_url = '/leaders'

    cookie = requests.get(f"{root_url}/{cookie_url}").cookies
    countries = requests.get(f"{root_url}/{countries_url}", cookies=cookie).json()

    session = requests.Session()
    for country in countries:
        cookie = requests.get(f"{root_url}/{cookie_url}").cookies
        leaders = requests.get(f"{root_url}/{leaders_url}", cookies=cookie, params={"country":country}).json()
        for leader in leaders:
            link = leader['wikipedia_url']
            leader['Paragraph'] = get_first_paragraph(link, session)

        
        leaders_per_country[country] = leaders
        
    return leaders_per_country


def save(leaders_per_country):
    with open("sample.json", "w") as outputfile: 
        json.dump(leaders_per_country, outputfile)

if __name__ == "__main__":
    leaders_per_country = get_leaders()
    save(leaders_per_country)