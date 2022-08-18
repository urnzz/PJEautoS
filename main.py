import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    options = uc.ChromeOptions()
    options.headless=True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)

    f = open("cpfs.txt", "r")
    cpfs = f.readlines()

    for cpf in cpfs:
        print("pesquisando "+cpf)
        driver.get("https://www.google.com/search?client=firefox-b-d&q=consulta+pje")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")))
        gs = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")
        gs.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')))
        cpfC = driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')
        cpfC.click()
        cpfC.clear()
        cpfC.send_keys(cpf)
        driver.find_element(By.XPATH, '//*[@id="fPP:searchProcessos"]').click()
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr')))
            t=driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody')
            rows = t.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                if "teto" in row.find_element(By.CLASS_NAME, "btn-block").text:
                    print('encontrado '+row.find_element(By.CLASS_NAME, "btn-block").text)
                else:
                    print('sem processo de teto')
        except:
            print("sem processo de teto") 
        driver.close()

if __name__ == '__main__':
    main()