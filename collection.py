"""Fetches all earthquakes in Iceland from 1995 from the Icelandic Met's office.
It's not optimal - could probably have used requests, but it works anyway.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import csv
import difflib
import time
import os
import pyperclip

global driver

try:
    options = Options()  # Formality
    options.headless = False  # Do not modify - otherwise key pressing won't work

    # options=options til að fá headless keyrslu
    driver = webdriver.Firefox(options=options,
                               service_log_path='nul')
    directory = os.getcwd()

    # Sækjum gögnin og vistum á réttum stað
    start_year = 1995
    end_year = 2021
    for year in range(start_year, end_year + 1):
        if not os.path.exists(directory + str(year)):
            os.mkdir(directory + str(year))
        for week in range(1, 53):
            print(str(year)+"."+str(week))
            # Dokum í max 30s áður en við hættum við
            driver.implicitly_wait(30)
            if week < 10:
                data_loc = f'http://hraun.vedur.is/ja/viku/{str(year)}/vika_0{str(week)}/listi'
                driver.get(data_loc)
            else:
                data_loc = f'http://hraun.vedur.is/ja/viku/{str(year)}/vika_{str(week)}/listi'
                driver.get(data_loc)
            driver.implicitly_wait(5)
            element = driver.find_element_by_xpath("/html/body")
            time.sleep(1)
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.CONTROL, "c")
            time.sleep(1)
            my_paste = pyperclip.paste()
            dest_file = f'{directory}{str(year)}/Earthquakes_{str(year)}_{str(week)}.txt'
            with open(dest_file, 'w') as f:
                f.write(my_paste)
    driver.quit()

except Exception as e:
    print(str(e))
    driver.quit()
    raise SystemExit
