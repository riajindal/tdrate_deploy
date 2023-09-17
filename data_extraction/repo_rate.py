from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re


def get_repo_rate():
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
    driver.get('https://www.rbi.org.in/')

    # Scraping Repo Rate
    repo_rate_raw = driver.find_element(By.XPATH, "//div[contains(@class, 'accordionContent')][1]//table//tr[1]//td[2]")

    # Get the inner text using execute_script
    text = driver.execute_script("return arguments[0].textContent;", repo_rate_raw)
    repo_rate = re.findall(r'\b\d+\.\d+\b', text)
    return float(repo_rate[0])

