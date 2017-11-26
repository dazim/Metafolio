import re
import requests
import csv
from lxml import html
import webbrowser
import time
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import matplotlib as mpl
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import codecs


wikipath = "/homes/ttreis/Code/Python/Metafolio/Alle wikifolios _ wikifolio.com.html"

def wikifolioLogin():

    payload = {
        "Username": "tim.treis@outlook.de",
        "Password": "waRFXAvACJGn"
    }

    session_requests = requests.session()
    login_url = "https://www.wikifolio.com/dynamic/de/de/login/login"
    result = session_requests.get(login_url)
    tree = html.fromstring(result.text)
    #authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    result = session_requests.post(
        login_url,
        data=payload,
        headers=dict(referer=login_url)
    )

    return result.status_code


def getAllWikifoliosFromFile(filepath):

    wikifolio_list = []

    infile = open(filepath, "r")

    reg = "class=\"wikifolio-preview-title-link\".href=\"(.*wf(.*))\">\n.*js-wikifolio-shortdescription\">(.*)<.span>"

    document_html = ""

    for line in infile:

        document_html += line

    wikifolios = re.findall(reg, document_html, re.MULTILINE)

    for wiki in wikifolios:

        wikifolio_list.append(list(wiki))

    return wikifolio_list


def downloadAllData(wikilist):

    for wiki in wikilist:

        i = 0

        while (wiki[1][i] == "0"):

            wiki[1] = wiki[1].replace("0", "", 1)

        print wiki[1]

        link = "https://www.wikifolio.com/dynamic/de/de/invest/download?type=daily&name=" + wiki[1] + "&dateFrom=01.01.2017&dateTo=26.11.2017"

        webbrowser.open(link)
        time.sleep(2)

def getAllFiles(path):

    return [f for f in listdir(path) if isfile(join(path, f))]

def getMonthlyPerformance(filelist):

    #for file in filelist:
    filepath = "/homes/ttreis/Code/Python/Metafolio/data/" + filelist[0]

    infile = open(filepath, "r")

    data = []

    for line in infile:
        data.append("".join(re.findall("[a-zA-Z0-9:,;\t\.]+", line)).split(";"))

    df = pd.DataFrame(data[6:], columns=["Begindate", "Timeintervalmin", "Open", "Close", "High", "Low"])

    df["Begindate"] = df['Begindate'].apply(lambda x: str(x)[0:10])

    return df


wikifolioLogin()


wikifolio_list = list(getAllWikifoliosFromFile(wikipath))
#print downloadAllData(wikifolio_list)

data_list = getAllFiles("/homes/ttreis/Code/Python/Metafolio/data/")

print getMonthlyPerformance(data_list)
print wikifolio_list
#https://www.wikifolio.com/dynamic/de/de/invest/download?type=daily&name=hgerp&dateFrom=01.01.2017&dateTo=26.11.2017