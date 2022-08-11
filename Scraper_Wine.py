import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pd.set_option('display.max_columns', 30)

database = pd.DataFrame()
database["name"]=np.nan

html_text = requests.get('https://lf-wines.ru/catalog/vina_po_otsenkam_i_otzyvam', verify=False).text
soup = BeautifulSoup (html_text,'lxml')
all_wine = soup.find_all("div",class_ = "col-xs-6 col-md-3")
last_page = soup.find_all("li",class_="")[-3].text
last_page = int(last_page)

for page in tqdm(range(1, last_page + 1)):

    url = 'https://lf-wines.ru/catalog/vina_po_otsenkam_i_otzyvam/?PAGEN_1=' + str(page)
    html_text = requests.get(url, verify=False).text
    soup = BeautifulSoup(html_text, 'lxml')
    all_wine = soup.find_all("div", class_="col-xs-6 col-md-3")

    for el in range(len(all_wine)):
        idx = len(database)
        title = all_wine[el].find("div", class_="product-item-title").text.replace("\t", "")
        title = title.replace("\n", "")

        database.loc[idx, "name"] = title
        href = all_wine[el].find("a", class_="product-item-image-wrapper")["href"]
        url = 'https://lf-wines.ru' + href
        html_text = requests.get(url, verify=False).text
        soup = BeautifulSoup(html_text, 'lxml')

        for i in range(len(soup.find_all("dd"))):

            name = soup.find_all("dt")[i].text
            value = soup.find_all("dd")[i].text

            if name not in database.columns:
                database[name] = np.nan

            database.loc[idx, name] = value

import datetime
name = "Wine_dataset " + str(datetime.datetime.now()).split(".")[-2]
database.to_csv(name, sep='\t', encoding='utf-8')