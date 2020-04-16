import pandas as pd
import sys

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://maps.google.com")

# wait for search box
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
search_box = driver.find_element_by_id('searchboxinput')

# search input
search_box.send_keys(sys.argv[1])
search_box.send_keys(Keys.ENTER)

# wait for complete search and results
WebDriverWait(driver, 100).until(EC.url_contains('search'))
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "pane")))
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "section-result-content")))
WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CLASS_NAME, "section-result-hours-phone-container")))
elem = driver.find_elements_by_class_name("section-result-text-content")

places = []
while True:
    try:
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
            if not data['phone_number']:
                continue
            places.append(data)

            # wait for next page button
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//button[@jsaction='pane.paginationSection.nextPage']")))

        try:
            next_page_btn = driver.find_element_by_xpath("//button[@jsaction='pane.paginationSection.nextPage']")
        except NoSuchElementException as e:
            break
        try:
            next_page_btn.click()
        except ElementClickInterceptedException as e:
            break
        if not next_page_btn.is_enabled():
            break
    except (ElementNotInteractableException, StaleElementReferenceException):
        break
driver.close()
telephones = []
result = []
# remove repeated entries
for p in places:
    tel = p['phone_number']
    if tel in telephones:
        continue
    else:
        result.append(p)
print(f'Found {len(result)} places.')
result = sorted(result, key=lambda k: k['place_type'])
# save to excel
df = pd.DataFrame(data=result)
df.columns = ['Nome', 'Tipo', 'Endereço', 'Horário', 'Telefone']
print(df.head())
try:
    df.to_excel(f'{sys.argv[1]}.xlsx')
except PermissionError:
    import random
    df.to_excel(f'{sys.argv[1]}-{random.randint(0, 100000)}.xlsx')

#
