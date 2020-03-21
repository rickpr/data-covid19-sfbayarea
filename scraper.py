#!/usr/bin/env python3
from bs4 import BeautifulSoup
from typing import Tuple, Dict, Callable
from county_info import counties
import requests
import pandas as pd
import datetime
import sys
import importlib

def get_html(url: str) -> BeautifulSoup:
    """
    Takes in a url string and returns a BeautifulSoup object
    representing the page
    """
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def format_single_digits(number: int) -> str:
    """
    Adds a leading zero to one digit numbers to make them line
    up with the existing data
    """
    if number < 10:
        return "0{0}".format(number)
    else:
        return str(number)

def format_year(year: int) -> int:
    """
    Turns a year into its short form e.g. 2020 -> 20
    """
    # get the short form of the year
    return year - 2000

def gen_date() -> str:
    """
    Generates today's date in MM/DD/YY format
    """
    today = datetime.datetime.today()
    month = format_single_digits(today.month)
    day = format_single_digits(today.day)
    year = format_year(today.year)

    return "{0}/{1}/{2}".format(month, day, year)

def format_time(timestamp: str) -> str:
    """
    Formats time in the format HH:MM:SS AM/PM
    """
    time, suffix = timestamp.split(' ')
    if len(time) == 4: # time is less than 10:00 w/ length 5
        time = '0{0}'.format(time)
    return '{0}:00 {1}'.format(time, suffix)

def gen_new_row_dict(dataframe: pd.DataFrame, num_cases: int, num_deaths: int, time_updated: str, city: str, county: str) -> Dict:
    """
    Generates a new row for a dataframe in dict format and calculates
    the new cases and deaths for the new data
    """
    cases_idx = 2
    deaths_idx = 4

    prev_cases = dataframe.iloc[-1, cases_idx]
    prev_deaths = dataframe.iloc[-1, deaths_idx]

    return {
        'date': gen_date(),
        'time_updated': format_time(time_updated),
        'total_positive_cases': num_cases,
        'new_daily_cases': (num_cases - prev_cases),
        'total_deaths': num_deaths,
        'new_daily_deaths': (num_deaths - prev_deaths),
        'city': city,
        'county': county,
        'state': 'CA'
    }

def scraper(county_info: Tuple[str, str, Callable, str, str]) -> None:
    """
    Puts together the other functions in this file to add new data from the
    specified URL (gathered according to data_getter) to the specified CSV
    """
    url, data_path, data_getter, city, county = county_info
    soup = get_html(url)
    print('Fetchind data from {0}'.format(url))
    cases, deaths, time = data_getter(soup)
    covid_data = pd.read_csv(data_path, dtype={'total_positive_cases': 'Int64', 'total_deaths': 'Int64'})
    new_row = gen_new_row_dict(covid_data, cases, deaths, time, city, county)
    covid_data = covid_data.append(new_row, ignore_index=True)
    print('Added the following row to {0}:'.format(data_path))
    print(covid_data.tail(1))
    covid_data.to_csv(data_path, index=False)

county_name = sys.argv[1]
# allows us to see all the columns of the new row
pd.set_option('display.max_columns', None)
scraper(counties[county_name])
