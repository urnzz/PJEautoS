import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    #files
    f = open("cpfs.txt", "r")
    cpfs = f.readlines()
    o = open('output.txt', 'w+')
    #pje search
    for cpf in cpfs:
        #browser setup
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        print("pesquisando "+cpf)
        #gseach
        driver.get("https://www.google.com/search?client=firefox-b-d&q=consulta+pje")
        while True:
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")))
                break
            except:
                pass
        gs = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")
        gs.click()
        #cpf keys
        while True:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')))
                break
            except:
                pass
        cpfC = driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')
        cpfC.click()
        cpfC.clear()
        cpfC.send_keys(cpf)
        #driver.find_element(By.XPATH, '//*[@id="fPP:searchProcessos"]').click()
        #check procs
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr')))
            t=driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody')
            rows = t.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                if "teto" or "Teto" in row.find_element(By.CLASS_NAME, "btn-block").text:
                    print('encontrado')
                    o.write(cpf+","+row.find_element(By.class_name, "btn-block").text)
                    break
                else:
                    print('sem processo de teto')
                    o.write(cpf+",sem processo de teto encontrado")
        except:
            print("sem processo de teto") 
        driver.close()

if __name__ == '__main__':
    main()