from bs4 import BeautifulSoup
import requests
from datetime import date
import re # regex
import supaBae

################################################
#### PROCESSING EVERY FIRM

firmsListUrl = "https://portal.myk.gov.tr/index.php?option=com_kurulus_ara&view=kurulus_ara"

firmsResult = requests.get(firmsListUrl)

firmsDoc = BeautifulSoup(firmsResult.text, "html.parser",from_encoding="tr-TR")

firmsMainLink = firmsDoc.find('tbody', attrs={'id': 'KursTbody'})

firmsList = []



for tr_values in firmsMainLink.findAll('tr'):
    firmNumber = tr_values.find('span')

    if re.match("FuncKurulus", firmNumber['onclick']):
        tempNumber = re.search('[0-9]+', firmNumber['onclick']).group()
        firmsList.append("https://portal.myk.gov.tr/index.php?option=com_kurulus_ara&view=kurulus_ara&layout=kurulus_tarife&kurId={}".format(tempNumber))


birimadi = ""
beforeName = ""
examPriceT1 = int()
examPriceP1 = int()

#### SINGLE FIRM PROCESS STARTS HERE

for eachFirm in firmsList:
    result = requests.get(eachFirm)
    doc = BeautifulSoup(result.text, "html.parser",from_encoding="tr-TR")
    mainLink = doc.find('div', attrs={'class': 'container-fluid'})

    firmName = mainLink.find('div', class_='col-12 baslik')
    print(firmName)
  
#### ScrapyPy 


    for spans in mainLink.findAll('div', class_="card border-primary"):  # Firmanın bütün yeterliliklerini getirir, WORKS,
        birimadi = spans.find("span", class_="mr-2").text.replace("/", "_")

        for type_values in spans.findAll('tr'):  # Firmanın bütün birimlerini ve fiyatlarını getirir, WORKS

            name = type_values.find('td', class_='align-middle')
            price = type_values.find('input', class_='form-control form-control-sm text-right')
            examType = type_values.find('td', class_='text-center')
            masteryType = type_values

            if (name == None):
                name = beforeName

            else:
                # print(name.get_text())
                beforeName = name.get_text()

            if (examType == None):
                continue

            priceFinal = price.get('value')

            if (examType.get_text() == "T1"):
                examPriceT1 = priceFinal
            else:
                examPriceP1 = priceFinal

            print(firmName.get_text(), birimadi, beforeName.replace("/", "_"), examPriceT1, examPriceP1)
            data = supaBae.supabase.table('kaan').insert({"firmName": f'{firmName.get_text()}',
                                                          "examName": f'{birimadi}',
                                                          "unitName": f'{beforeName.replace("/", "_")}',
                                                          "priceT1": examPriceT1,
                                                          "priceP1": examPriceP1
                                                          }).execute()
