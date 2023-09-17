from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import re

# WEB SCRAPING

# Web scraping prerequisites and configuration
web_service = Service('/usr/local/bin/chromedriver.exe')
url_kotak = 'https://www.paisabazaar.com/fixed-deposit/kotak-mahindra-bank-fd-rates/'
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dve-shm-uage')

driver = webdriver.Chrome(service=web_service, options=options)
driver.get(url_kotak)

# Scraping Tenure v/s Interest Rate Table
kotak_tenure_rates = []
element_found = False
i = 0

while not element_found:
    try:
        tenure = driver.find_element(By.XPATH,
                                     "//div[contains(@class, 'wpb_text_column')][2]//tr[" + str(
                                         i + 3) + "]//td[1]").text
        general_rate = driver.find_element(By.XPATH,
                                           "//div[contains(@class, 'wpb_text_column')][2]//tr[" + str(
                                               i + 3) + "]//td[2]").text
        senior_rate = driver.find_element(By.XPATH,
                                          "//div[contains(@class, 'wpb_text_column')][2]//tr[" + str(
                                              i + 3) + "]//td[3]").text

        item = {
            'Tenure': tenure,
            'General Rate': general_rate,
            'Senior Rate': senior_rate,
        }

        kotak_tenure_rates.append(item)
        i += 1

    except NoSuchElementException:
        element_found = True
        break

# Storing table in a dataframe
df_1 = pd.DataFrame(kotak_tenure_rates)


# CLEANING THE WEB SCRAPED DATA
df_1['Tenure'] = df_1['Tenure'].astype(str)


def format_tenure(value):
    value = value.replace("–", "-")
    value = value.replace("to", "-")
    p = r'\([^)]*\)'
    value = re.sub(p, '', value)

    return value


# Using format function on Tenure to
# bring it to a standard format of notation
df_1['Tenure'] = df_1['Tenure'].apply(format_tenure)

# Creating a Min Value and Max Value column
# by splitting the Tenure column at '-'
df_1[['Min Value', 'Max Value']] = df_1['Tenure'].str.split('-', expand=True)

# Replacing None/NaN with 0 from Max Value Column
# if range is a single date e.g. 180 days
# and converting the value to a string
df_1['Max Value'] = df_1['Max Value'].fillna(0)
df_1['Max Value'] = df_1['Max Value'].astype(str)

if df_1['General Rate'].dtype != float:
    df_1['General Rate'] = df_1['General Rate'].apply(lambda x: x.replace("%", ""))
    df_1['General Rate'] = df_1['General Rate'].astype(float)


# Custom function to transform time period
# in words to number of days format
def convert_to_days(duration):
    days = 0
    if duration is None:
        return 0
    flag = re.findall(r"less than", duration)
    matches = re.findall(r'(\d+)\s*(days?|months?|years?)', duration, re.IGNORECASE)
    for match in matches:
        value, unit = match
        if unit.lower() in ['day', 'days']:
            days += int(value)
        elif unit.lower() in ['month', 'months']:
            days += int(value) * 30  # Assuming 30 days in a month
        elif unit.lower() in ['year', 'years']:
            days += int(value) * 365  # Assuming 365 days in a year
            if flag:
                days -= 1

    if not matches:
        try:
            days += int(duration)
        except ValueError:
            pass

    return days


# Convert Min and Max Value columns
# to number of days format
df_1['Min Value'] = df_1['Min Value'].apply(convert_to_days)
df_1['Max Value'] = df_1['Max Value'].apply(convert_to_days)

# If Max Value column contains 0 then replacing
# it with respective Min Value column value
df_1.loc[df_1['Max Value'] == 0, 'Max Value'] = df_1.loc[df_1['Max Value'] == 0, 'Min Value']


# Checking whether Min Value and Max Value
# columns are transformed as required
result = pd.concat([df_1['Min Value'], df_1['Max Value']], axis=1)
# print(result)

# Storing dataframe as csv file
df_1.to_csv('kotak_slabs.csv', index=False, mode='w')
