from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.worldometers.info/coronavirus/";

html_content = requests.get(url).text

soup = BeautifulSoup(html_content,"html")

table = soup.find('table', attrs={'id':'main_table_countries_today'})

table_body = table.find('tbody');


rowsToSkip = table_body.find_all("tr", {"style": "display: none"})

rows = []
for row in table_body.find_all("tr"):
    if row in rowsToSkip:
        continue
    rows.append(row)



i=0
data = []
for row in rows:

    cols = row.find_all('td')
    i = i + 1

    colData = []
    colData.append(cols[1].text)
    if len(cols[2].text.strip()) > 0:
        case = cols[2].text.replace(",","").strip()
        if case == 'N/A':
            case = 0
        colData.append(int(case))
    else:
        colData.append(0)

    if len(cols[4].text.strip()) > 0:
        deaths = cols[4].text.replace(",","").strip()
        if deaths == 'N/A':
            deaths = 0
        colData.append(int(deaths))
    else:
        colData.append(0)

    if len(cols[6].text.strip()) > 0:
        recovered = cols[6].text.replace(",","")
        if recovered == 'N/A':
            recovered = 0
        colData.append(int(recovered))
    else:
        colData.append(0)

    data.append(colData)

for d in data:
    print(d)

# writing csv file
fields = ['Country', 'Total Cases', 'Total Deaths', 'Total Recovered']
filename = "world_covid_data.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(data)
