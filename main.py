import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

f = open("cpfs.txt", "r")
cpfs = f.readlines()
driver = webdriver.Firefox(firefox_profile=r".\Profile", executable_path=r".\geckodriver.exe")

for cpf in cpfs:
    driver.get("https://www.google.com/search?client=firefox-b-d&q=consulta+pje")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")))
    gs = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")
    gs.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')))
    cpfC = driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')
    cpfC.click()
    cpfC.clear()
    cpfC.send_keys(cpf)
    driver.find_element(By.XPATH, '//*[@id="fPP:searchProcessos"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr')))
    driver.close()