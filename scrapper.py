#Project 2: Web scraper using BeautifulSoup4 and requests
import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max",help="Enter the number of pages to parse", type=int)
parser.add_argument("--dbname",help="Enter the number of pages to parse",type=int)
args = parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = args.page_num_max
scraped_info_list = []
connect.connect(args.dbname)

for page_num in range(1,page_num_MAX):
  req = requests.get(oyo_url + str(page_num))
  content = req.content

  soup = BeautifulSoup(content,"html.parser")
  all_hotels = soup.find_all("div",{"class":"hotelCardListing"})

  for hotels in all_hotels:
    hotel_dict = {}
    hotel_dict["name"] = hotel.find("h3",{"class": "listingHotelDescription_hotelName"}).text
    hotel_dict["address"] = hotel.find("span", {"itemprop":"streetAddress"}).text
    hotel_dict["price"] = hotel.find("span", {"class": "listingPrice_finalPrice"}).text
    #try....except
    try:
      hotel_dict["rating"] = hotel.find("span",{"class": "hotelRating__ratingSummary"}).text
      except AttributeError:
        pass
        
        parent_amenities_element = hotel.find("div",{"class":"amenityWrapper"})

        amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())

        hotel_dict["amenities"] = ','.join(amenities_list[:-1])

        scraped_info_.append(hotel_dict)
        connect.insert_into_table(args.dbname,tuple(hotel_dict.values()))
        
        # print(hotel_name,hotel_addresss,hotel_price,hotel_rating,amenties_list)

        dataFrame = pandas.DataFrame(hotel_dict)
        dataFrame.to_csv("Oyo.csv")
        connect.get_hotel_info(args.dbname)




#databases: organized collection of data,generally stored and accessed electronically
# sql: structured query language
# pip install db-sqLite3
import sqLite3
def connect(dbname):
  conn = sqlLite3.connect(dbname)
conn.execute("CREATE TABLE IF NOT EXISTS OYO_HOTELS (NAME TEXT,ADDRESS TEXT, PRICE INT,AMENITIES TEXT,RATING TEXT)")
print("Table created successfully!")
conn.close()
def insert_into_table(dbname,values):
  conn = sqLite3.connect(dbname)
conn.execute("INSERT INTO OYO_HOTELS (NAME,ADDRESS,PRICE,AMENITIES,RATING) VALUES (?,?,?,?,?)")

conn.execute(insert_sql,values)

conn.commit()
conn.close()
def get_hotel_info(dbname):
  conn = sqLite3.connect(dbname)

cur = conn.cursor()

cur.execute("SELECT * FROM OYO_HOTELS")
table_data = cur.fetchall()

for record in table_data:
  print(record)
