# _*_coding: utf-8_*_

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sqlite3

def Database():

    global conn, cursor
    conn = sqlite3.connect("RecaiMain.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `scrapedData` (entry_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, entry_content TEXT, suser_name TEXT, entry_date TEXT, entry_valid)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `autoData` (auto_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, auto_brand TEXT, auto_model TEXT, engine_type TEXT)")
    if cursor.fetchone() is None:
        conn.commit()


def getEntries():

    links = []
    entries = []
    susers = []
    datetime = []
    linkstarter = "https://eksisozluk.com/eksi-sozluk-yakit-tuketimi-veritabani--3649746?p=1"
    linkincrease = linkstarter[:-1]
    for index in range(1, 406):
        linkbuilt = linkincrease + str(index)
        links.append(linkbuilt)

    browser = webdriver.Firefox()

    for link in links:
        browser.get(link)
        html = browser.page_source
        time.sleep(2)
        soup = BeautifulSoup(html, 'html.parser')
        entry_area = soup.find("ul", {"id": "entry-item-list"})
        contents = entry_area.find_all("div", class_="content")
        authors = entry_area.find_all("a", class_="entry-author")
        dates = entry_area.find_all("a", class_="entry-date permalink")

        for idx in range(len(contents)):
            entries.append(contents[idx].text.replace("\n", ""))
            susers.append(authors[idx].text)
            datetime.append(dates[idx].text)
            print(contents[idx].text)
            print(authors[idx].text)
            print(dates[idx].text)

    scrapedData ={
      "entry": entries,
      "suser": susers,
      "datetime": datetime
    }

    Database()
    for indx in range(len(scrapedData["entry"])):
        cursor.execute(
            "INSERT INTO `scrapedData` (entry_content, suser_name, entry_date) VALUES(?, ?, ?)",
            (scrapedData["entry"][indx], scrapedData["suser"][indx], scrapedData["datetime"][indx]))
        conn.commit()
    cursor.close()
    conn.close()
    browser.close()

def getAutoData():

    links = []
    brands = []
    models = []
    engines = []

    linkstarter = "https://www.autoevolution.com/cars/"

    browser = webdriver.Firefox()
    browser.get(linkstarter)
    html = browser.page_source
    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')

    for i in soup.find_all("span", {"itemprop": "name"}):
        if i.text == 'Home' or i.text == 'Cars':
            continue
        else:
            brands.append(i.text)
            print(i.text)

    for brand in brands:
        if " " in brand:
            brand = brand.replace(" ", "-")
        linker = linkstarter[:-5] + brand.lower()
        links.append(linker)

    for link in links:
        browser.get(link)
        html = browser.page_source
        time.sleep(2)
        soup = BeautifulSoup(html, 'html.parser')
        modelnames = soup.find_all("h4")
        enginetype = soup.find_all("p", class_="eng")

        for idx in range(len(modelnames)):
            models.append(modelnames[idx].text)
            print(modelnames[idx].text)
            a = enginetype[idx].find_all("span")
            if len(a) == 0:
                engine = "NA"
            elif len(a) > 1:
                for ind in range(len(a)):
                    if ind == 0:
                        engine = a[ind].text
                    else:
                        engine = engine + " " + a[ind].text
            else:
                engine = a[0].text
            engines.append(engine)
            print(engine)

    browser.close()

    autoData ={
      "models": models,
      "engines": engines,
    }

    Database()
    for indx in range(len(autoData["models"])):
        cursor.execute(
            "INSERT INTO `autoData` (auto_model, engine_type) VALUES(?, ?)",
            (autoData["models"][indx], autoData["engines"][indx]))
        conn.commit()
    cursor.close()
    conn.close()

def checkValidity():

    Database()
    match_number = 0
    cursor.execute("SELECT entry_content FROM `scrapedData`")
    entries = cursor.fetchall()
    cursor.execute("SELECT auto_model FROM `autoData`")
    models = cursor.fetchall()
    for idx in range(len(entries)):
        for i in range(len(models)):
            if models[i][0].lower() in entries[idx][0]:
                match_number += 1
            else:
                continue

    cursor.close()
    conn.close()

    validity_rat =match_number/(len(entries))

    print("Valid entries for analysis:" + str(match_number))
    print("Validity ratio:" + str(validity_rat))

checkValidity()