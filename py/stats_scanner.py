import os
import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from time import sleep

os.chdir("/mnt/aec0936f-d983-44c1-99f5-0f5b36390285/Dropbox/Python/Predictive Analytics FIFA")
'''
browser = webdriver.Firefox()

browser.get("https://www.whoscored.com/Regions/247/Tournaments/36/Seasons/5967/Stages/15737/Show/International-FIFA-World-Cup-2018")

sleep(3)
 
base_url = 'https://www.whoscored.com'

def get_countries_links(browser):
    return [team.get_attribute('href') for team in browser.find_elements_by_xpath('//table[@id="tournament-fixture"]//td[contains(@class,"team")]//a')]

countries_link = set()
countries_link.update(get_countries_links(browser))


browser.find_elements_by_xpath('//table[@id="tournament-fixture"]//td[contains(@class,"team")]//a')[0].get_attribute('href')

# click next page

browser.find_element_by_xpath('//span[contains(@class, "ui-icon-triangle-1-e")]').click()

sleep(1)

countries_link.update(get_countries_links(browser))

# click next page

browser.find_element_by_xpath('//span[contains(@class, "ui-icon-triangle-1-e")]').click()

sleep(1)

countries_link.update(get_countries_links(browser))

  
#countries_link


player_link = dict()

for country_link in countries_link:
    browser.get(country_link)
    sleep(1)
    team = browser.find_element_by_xpath('//span[@class="team-header-name"]')
    player_link[team.text] = dict()    
    for player in browser.find_elements_by_xpath('//table[@id="top-player-stats-summary-grid"]//tbody//tr//a'):
        player_link[team.text][player.text] = player.get_attribute('href')

 
np.save("Data/player_link.npy", player_link)
'''
def detect_element(browser, element_id, by_what = By.ID):
    # Simplify the detection of an element in the browser
    
    element_present = EC.presence_of_element_located((by_what, element_id))

    try:
        WebDriverWait(browser, 5, poll_frequency = .1).until(element_present)
        return True
    
    except TimeoutException as e:
        return False

player_link = np.load("Data/player_link.npy").item()

# will delete nan from already_loaded
already_loaded = rating_dict.copy()
for team in rating_dict.keys():
    for player in rating_dict[team]:
        if pd.isnull(rating_dict[team][player]):
            already_loaded[team].pop(player, None)

#caps = DesiredCapabilities().FIREFOX
caps = DesiredCapabilities.CHROME
caps["pageLoadStrategy"] = "none"

#rating_dict = {team:{} for team in player_link.keys()}

browser = webdriver.Chrome(desired_capabilities = caps)#Firefox(capabilities=caps)

for team in player_link.keys():
    for player in player_link[team].keys():
        if player in already_loaded[team].keys(): continue
    
        while True:
            try:
                browser.get(player_link[team][player])
                wait = WebDriverWait(browser, 20)
                wait.until(EC.presence_of_element_located((By.XPATH, '//table[@id="top-player-stats-summary-grid"]')))
                browser.execute_script("window.stop();")
                
                try:
                    rating_dict[team][player] = browser.find_elements_by_xpath('//table[@id="top-player-stats-summary-grid"]//td[@class="rating"]')[-1].text
                    print(rating_dict[team][player])
                    break
                except IndexError:
                    try:
                        iframe = browser.find_element_by_xpath('//iframe')
                        browser.switch_to_frame(iframe)
                        browser.find_element_by_xpath('//p[contains(text(), "Access Denied")]')
                        sleep(5)
                    except NoSuchElementException: 
                        rating_dict[team][player] = np.nan
            except TimeoutException:
                sleep(5)
            
np.save("Data/rating_dict.npy", rating_dict)

rating_dict['Saudi Arabia']


