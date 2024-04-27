import json
import re
from dataclasses import dataclass
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

investor_data_list = []

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
)


def get_parse_signal():
    count = 0
    driver = webdriver.Chrome(options=options)

    driver.get("https://signal.nfx.com/investor-lists/top-fintech-seed-investors")

    for _ in range(600):
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".btn-xs.sn-light-greyblue-accent-button.sn-center.mt3.mb2.btn.btn-default",
                    )
                )
            )
            load_more_button.click()

            sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    response = driver.page_source

    with open("signal.html", "w") as file:
        file.write(response)

    with open("signal.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    a_tags = soup.find_all("a", class_="flex-column pt1 mr3 items-center")

    investor_urls = []
    for a in a_tags:
        href = a.get("href")
        if href:
            count += 1
            investor_url = "https://signal.nfx.com" + href
            investor_urls.append(investor_url)

        print(count)

    with open("signal_investor_urls.json", "w") as file:
        json.dump(investor_urls, file, indent=4)


get_parse_signal()
