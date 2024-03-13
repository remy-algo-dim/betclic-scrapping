from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from dotenv import load_dotenv
import os

import scrapping
import utils
import send_mail

load_dotenv()

MAIL = os.getenv('MAIL')
PSWD = os.getenv('PSWD')

ENVIRONMENT = os.getenv('ENVIRONMENT')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
print("CHROMEDRIVER_PATH: {}".format(CHROMEDRIVER_PATH))
print("ENVIRONMENT: {}".format(ENVIRONMENT))

betclic_url = "https://www.betclic.fr/top-football-europeen-s1/top-football-europeen-p1"


def start_selenium(CHROMEDRIVER_PATH, betclic_url):
    """
    Open betclic url via Selenium
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    if ENVIRONMENT == 'production':
        chrome_options.add_argument("--headless")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(betclic_url)
    return driver


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        # Full Pipeline
        driver = start_selenium(CHROMEDRIVER_PATH, betclic_url)
        print("Selenium well started")
        print(100*"=")
        time.sleep(3)

        scrapping.accept_user_conditions(driver)
        print("Success to accept users conditions")
        print(100*"=")
        time.sleep(3)

        all_bets = utils.retrieve_all_bets(driver, betclic_url)
        df = utils.create_dataframe(all_bets)
        print(df)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'data.csv')
        df_loaded = pd.read_csv(csv_file_path, index_col='Index')
        df_final = pd.concat([df_loaded, df])
        df_final.to_csv(csv_file_path, index_label='Index')
        print(df)
        send_mail.send_notifications(MAIL, [MAIL],
                                     "Scrap updated", csv_file_path)
        print("**** END SUCCESS ****")
    except Exception as e:
        print(e)
        send_mail.send_notifications(MAIL, [MAIL],
                                     "Error when scrapping Betclic")

