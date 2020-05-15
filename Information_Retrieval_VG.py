import requests
from bs4 import BeautifulSoup
import csv
import re

r = requests.get("https://www.blocket.se/annonser/uppsala/fordon/bilar?cg=1020&r=10")
soup = BeautifulSoup(r.text, "html.parser")

# prepare the csv file to write
save_name = "blocket_car_ads.csv"
with open(save_name, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, dialect='excel')

    #extract the whole tag which talks about the product.   
    pattern="[A-Z]"
    ads_dict = {}
    for line in soup.find_all("div", class_="styled__Content-sc-1kpvi4z-2 hdKKry"):
        # get the information we need to store about each advertisement.
        # divide the line by Upper class words
        info = re.sub(pattern,lambda x:" "+x.group(0),line.contents[0].get_text())
        info = info.split(" ")
        location = info[-3]
        time = info[-1]+info[-2]
        # title is in the second line
        title = line.contents[1].get_text()
        # advertisemen 
        ads_text = line.contents[2].get_text()
        price_ID = line.contents[3].get_text().split("kr")
        ID = price_ID[-1]
        ID = ID.split(")")[-1]
        price = price_ID[0]    
        # write the information in the csv file.
        writer.writerow([location])
        writer.writerow([time])
        writer.writerow([title])
        writer.writerow([ads_text])
        writer.writerow([ID])
        writer.writerow([price])
        
f.close()
