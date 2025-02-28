import re
import sys
from zeep import Client
from datetime import datetime
import math
from tabulate  import tabulate
from bs4 import BeautifulSoup
import requests

def get_vested_stocks():
    try:
        vested_stocks = int(input("Number of stocks vested: "))
    except ValueError:
        sys.exit("Please enter an integer as input.")
    else:
        return vested_stocks


def get_date():
    vest_date = input('Date when the stocks vested (format: YYYY-MM-DD): ')
    pattern = r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$"
    matches = re.match(pattern, vest_date)
    if matches:
        if 1948 < int(matches.group('year')) <= datetime.now().year and 0 < int(matches.group('month')) < 13 and 0 < int(matches.group('day')) < 32:
            return matches.group(0)

        else:
            sys.exit('Incorrect date ranges - Year should start from 1949, should not be later that the current year, month should be between 1-12, date should be between 1-31')
    else:
        sys.exit('Incorrect date input. Usage: YYYY-MM-DD')


def get_current_rate(date):

    try:

        wsdl = 'http://www.mnb.hu/arfolyamok.asmx?wsdl'
        client = Client(wsdl=wsdl)
        result = client.service.GetExchangeRates(startDate=date, endDate=date, currencyNames='GBP,HUF')

    except Exception:
        #Webscraping fallback

        print('Previous try failed with MNB SOAP API, trying fallback method. Please reenter the date. ')
        date = get_date().replace('-','.')
        url = f"https://www.mnb.hu/arfolyam-tablazat?deviza=rbCurrencySelect&devizaSelected=GBP&datefrom={date}.&datetill={date}.&order=1"
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        findings = soup.find_all('td')
        pattern = r"\d{3},\d{1,2}"
        matches = re.search(pattern, str(findings[1]))
        if matches:
            return float(matches.group(0).replace(',','.'))
        else:
            raise ValueError('No booked rate on specified date, possibly not a business day')

    else:

        pattern = r'^<MNBExchangeRates ?\/?>(<Day date="\d{4}-\d{2}-\d{2}"><Rate unit="1" curr="GBP">)?(?P<exchange_rate>\d{3},\d{1,2})?(<\/Rate><\/Day><\/MNBExchangeRates>)?$'
        matches = re.match(pattern, result)
        if matches and matches.group('exchange_rate'):
            return float(matches.group('exchange_rate').replace(',','.'))
        else:
            raise ValueError('No booked rate on specified date, possibly not a business day')



def fetch_exchange_rate():
    date = get_date()
    for _ in range(2):
        try:
            return get_current_rate(date)
        except ValueError:
            print('No booked rate on specified date, possibly not a business day. Try another date. ')
            date = get_date()
    print('Unable to get rate, quitting the program. ')
    return None


def calculate_tax(vested_stocks, rate, release_price):

    szja = vested_stocks * rate * release_price * 0.89 * 0.15
    szocho = vested_stocks * rate * release_price * 0.89 * 0.13
    return szja, szocho

def get_release_price():
    try:
        return float(input('Release price(found in ShareWorks, in Okta, format example: 9.010202): '))
    except ValueError:
        sys.exit("Please specify the release price. Usage format example: 9.010202")


def main():

    vested_stocks = get_vested_stocks()
    rate = fetch_exchange_rate()
    if rate is None:
        sys.exit()

    release_price = get_release_price()
    szja, szocho = calculate_tax(vested_stocks, rate, release_price)

    format = [['SZJA', f"{math.ceil(szja)} HUF"], ['SZOCHO', f"{math.ceil(szocho)} HUF"]]


    print(tabulate(format))
    print(f"Note: The amounts are rounded up, to the nearest integer. The more precise values are {szja} and {szocho}. ")


if __name__ == "__main__":
    main()


