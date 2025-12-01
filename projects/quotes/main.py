import requests
from bs4 import BeautifulSoup
import pandas as pd


page = requests.get("https://quotes.toscrape.com/")

def get_quotes(pageUrl):
    page = requests.get(pageUrl)
    parsedPage = BeautifulSoup(page.content, "lxml")
    quotes = parsedPage.find_all('div',{'class':'quote'})
    if len(quotes) > 0:
        quotes_list = [extract_data(quote) for quote in quotes]
        return quotes_list
    else:
        return None

def extract_data(div_quotes):
    quote  = div_quotes.find('span',{'class':'text'}).get_text()
    author = div_quotes.find('small',{'class':'author'}).get_text()
    tags   = [tag.get_text() for tag in div_quotes.find_all('a',{'class':'tag'})]
    data   = {
    'quote' :quote,
    'author':author,
    'tags'  :tags
    }
    return data

if page.status_code == 200:
    parsedPage = BeautifulSoup(page.content, "lxml")

data = get_quotes("https://quotes.toscrape.com/")
#quotes_list = []
for i in range(2,100):
    print(f"Scraping page {i}... Waiting.")
    page_url = f"https://quotes.toscrape.com/page/{i}/"
    current_page = get_quotes(page_url)
    if current_page is not None:
        data = data + current_page
    else:
        break

quotes_list = data
print(quotes_list)
df = pd.DataFrame(quotes_list)
print(df)
df.to_csv('projects/quotes/quotes.csv',index=False,encoding='utf-8')
df.to_excel('projects/quotes/quotes.xlsx',sheet_name='Quotes',index=False,engine='openpyxl')
df.to_json('projects/quotes/quotes_df.json',orient='records',force_ascii=False,indent=4)