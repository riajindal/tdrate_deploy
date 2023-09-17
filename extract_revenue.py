from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from utility import master
import re


def get_revenue(bank, code):
    # WEB SCRAPING

    # Web scraping prerequisites and configuration
    web_service = Service()

    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dve-shm-uage')

    driver = webdriver.Chrome(service=web_service, options=options)
    url = 'https://finance.yahoo.com/quote/'+code+'/financials?p='+code
    driver.get(url)

    # From financials section of Yahoo Finance extract the revenue generated
    # in terms of total income and interest income
    ttm = driver.find_element(By.XPATH, '//div[contains(@id, "Col1-1-Financials-Proxy")]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[2]/span').text
    button = driver.find_element(By.XPATH, '//div[contains(@id, "Col1-1-Financials-Proxy")]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/button')
    button.click()
    interest_income = driver.find_element(By.XPATH, '//div[contains(@id, "Col1-1-Financials-Proxy")]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span').text
    bank.ttm = ttm
    bank.interest_income = interest_income
    print(bank.name)


# if __name__ == '__main__':
    # get_revenue('https://finance.yahoo.com/quote/ICICIBANK.NS/financials?p=ICICIBANK.NS')

# Since running this script multiple times is time-consuming
# and slows down the processes a function is created
# to store the retrieved data in a .csv file for faster access
def faster_get_revenue(master):
    data = []
    for bank in master:
        data.append({
            'Bank Name': bank.name,
            'TTM': bank.ttm,
            'Interest Income': bank.interest_income
        })

    df = pd.DataFrame(data)
    print("Revenue extracted")
    df.to_csv('bank_revenue.csv', mode='w', index=False)


if __name__ == '__main__':
    for bank in master:
        get_revenue(bank, bank.id)

    faster_get_revenue(master)


