import json
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://maps.google.com")

WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
search_box = driver.find_element_by_id('searchboxinput')
search_box.send_keys('empresa')
search_box.send_keys(Keys.ENTER)

WebDriverWait(driver, 100).until(EC.url_contains('search'))
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "pane")))
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "section-result-content")))
WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CLASS_NAME, "section-result-hours-phone-container")))
elem: List[WebElement] = driver.find_elements_by_class_name("section-result-text-content")
el: WebElement
places = []

while True:
    for el in elem:
        data = {}
        data['name'] = el.find_element_by_css_selector('.section-result-title span').text
        data['place_type'] = el.find_element_by_css_selector('.section-result-details').text
        data['place_address'] = el.find_element_by_css_selector('.section-result-location').text
        try:
            data['opening_hour'] = el.find_element_by_css_selector('.section-result-opening-hours span').text
        except NoSuchElementException:
            data['opening_hour'] = None
        try:
            data['phone_number'] = el.find_element_by_css_selector('.section-result-phone-number span').text
        except NoSuchElementException:
            continue
        places.append(data)
    try:
        next_page_btn = driver.find_element_by_xpath("//button[@jsaction='pane.paginationSection.nextPage']")
    except NoSuchElementException as e:
        print(e)
        break
    try:
        next_page_btn.click()
    except ElementClickInterceptedException as e:
        print(e)
        break
    if not next_page_btn.is_enabled():
        break
print(f'Found {len(places)} places.')
with open('data.json', 'w') as f:
    f.write(json.dumps(places, indent=2))
driver.close()
