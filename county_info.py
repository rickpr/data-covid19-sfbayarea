from bs4 import BeautifulSoup
from typing import Tuple
import re


def find_tags_sf(soup: BeautifulSoup) -> Tuple[int, int, str]:
    """
    Takes in a BeautifulSoup object and returns a tuple of the number
    of cases (int), the number of deaths (int) and the time that the
    data was updated(str)
    """
    helpful_links_box = soup.find(id='helpful-links')

    cases_regex = re.compile('Total Positive Cases: ([\d,]+)')
    deaths_regex = re.compile('Deaths: ([\d,]+)')
    time_regex = re.compile('updated daily at (\d{1,2}:\d{1,2} (AM|PM))')

    cases_html = soup.find('p', text=cases_regex)
    deaths_html = soup.find('p', text=deaths_regex)
    time_html = soup.find('p', text=time_regex)

    num_cases = int(re.match(cases_regex, cases_html.text).group(1))
    num_deaths = int(re.match(deaths_regex, deaths_html.text).group(1))
    time_updated = re.match(time_regex, time_html.text).group(1)
    return (num_cases, num_deaths, time_updated)

counties = {
    'san-francisco': (
        'https://www.sfdph.org/dph/alerts/coronavirus.asp',# url
        'data/covid_19_sf.csv', # data_path
        find_tags_sf, # data_getter
        'San Francisco', # city
        'San Francisco', # county
    ),
    'santa-clara':()
}
