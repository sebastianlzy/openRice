#!/usr/bin/python
# -*- coding: utf8 -*-

# READ ME
#Data will be loaded on a yearly basis. This script takes in an argument, year and will automatically return the result for the whole of that year
#Run python currency_scrape.py [year]
#

from bs4 import BeautifulSoup
from urllib import urlencode
from urllib2 import urlopen
from selenium import webdriver
import unicodecsv as csv
import datetime
import sys
import re


# HOME_URL= "http://my.openrice.com"

# 1. CHANGE THE HOME URL
HOME_URL= "http://tw.openrice.com"
# 2. CHANGE THE TOTAL NUMBER OF RESTAURANT
TOTAL_NUMBER_OF_RESTAURANT = 400


BROWSER = webdriver.Firefox()
LAST_PAGE = (TOTAL_NUMBER_OF_RESTAURANT/15 + 1)

def main():

    for number in range(3,LAST_PAGE):
        print "Scraping page {number} of {last_page}".format(number=number,last_page=LAST_PAGE)
        write_restaurant_address_to_csv(get_url_for_(HOME_URL, number),number)
    BROWSER.quit()


def write_to_csv(file_name, arr_objs):
    with open(file_name, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, encoding="utf-8")
        for arr_obj in arr_objs:
            try:
                csv_writer.writerow(arr_obj)
            except UnicodeEncodeError:
                print "cant write ", arr_obj, " into file"


def get_url_for_(home_url, number):
    # 3. CHANGE TO THE URL THAT YOU WANT
    # return home_url + "/klangvalley/restaurants/district/kuala-lumpur?page={number}&searchSort=31&region=500&district_id=1999&amenity_id=1002".format(number=number)
    # return home_url + "/klangvalley/restaurants/district/kuala-lumpur?page={number}&searchSort=31&region=500&district_id=1999&condition=%2Cdelivery&amenity_id=1003".format(number=number)
    # return home_url + "/klangvalley/restaurants/district/kuala-lumpur?page={number}&searchSort=31&region=500&district_id=1999&condition=%2Cdelivery".format(number=number)
    return home_url + "/northern/restaurants/district/{chinese}?page={number}&searchSort=31&region=700&district_id=1999&amenity_id=1003".format(number=number,chinese="%E5%8F%B0%E5%8C%97%E5%B8%82")
    # return home_url + "/northern/restaurants/district/{chinese}?page={number}&searchSort=31&region=700&district_id=1999&amenity_id=1003".format(number=number,chinese="u\'台北市'")



def write_restaurant_address_to_csv(url,number):
    try:
        print url
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        rest_lists = soup.find_all(class_='sr1_poi_title')
        rest_data = []
        for rest_list_index, rest_list in enumerate(rest_lists):
            rest_link = rest_list.find('a').get('href')
            rest_name = rest_list.find('a').contents[0].string
            rest_datum = [rest_name,get_number_from_link(rest_link),get_website_from_link(rest_link)]
            print rest_datum
            rest_data.append(rest_datum)

        write_to_csv("restaurants_url_{number}.csv".format(number=number),rest_data)
    except:
        print "Unexpected error:", sys.exc_info()[0]


def get_number_from_link(url_link):
    html = urlopen("{home_url}{url}".format(home_url=HOME_URL,url=url_link)).read()
    soup = BeautifulSoup(html)
    rest_details = soup.find(class_='sprite-global-icon2')

    try:
        number = rest_details.next_element.next_element.string
    except AttributeError:
        number = "No number"
    return number

def get_website_from_link(url_link):
    html = urlopen("{home_url}{url}".format(home_url=HOME_URL,url=url_link)).read()
    soup = BeautifulSoup(html)
    rest_details = soup.find(class_='sr2_website_nowrap')
    try:
        website = rest_details.get('href')
    except AttributeError:
        website = "No website"
    return website

def write_to_csv_rest(file_name, arr_objs):
    with open(file_name, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, encoding="utf-8")
        try:
            csv_writer.writerow(arr_objs)
        except UnicodeEncodeError:
            print "cant write ", arr_objs, " into file"



if __name__ == '__main__':
    main()






















