import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading
import csv

def T(num, t, writer, reader):
    for i in range(num):
        row_count = sum(1 for row in reader)
        n=row_count/num
        cpfs=[]
        for a in range((n*i)-(n*(i-1)):
            cpfs.append(a)
        th=threading.Thread(target=S, args=(writer, reader, cpfs))
        th.start()
        t.append(th)

def S(writer, reader, cpfs):
    n=0
    for cpf in cpfs:
        print(n+' de '+len(cpfs))
        try:
            options = uc.ChromeOptions()
            options.headless=True
            driver = uc.Chrome(options=options)
            print("pesquisando no PJE "+cpf.strip())
            driver.get("https://www.google.com/search?client=firefox-b-d&q=consulta+pje")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/a/h3')))
            gs = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/a/h3')
            gs.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')))
            cpfC = driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')
            cpfC.click()
            cpfC.clear()
            for i in cpf.strip():
                cpfC.send_keys(i)
            driver.find_element(By.XPATH, '//*[@id="fPP:searchProcessos"]').click()
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr')))
                t=driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody')
                rows = t.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    f= str(row.text)
                    if "teto" in f:
                        print('encontrado')
                        writer.writerow([cpf.strip(),f.strip()])
                        break
                    else:
                        if "Teto" in f:
                            print('encontrado')
                            writer.writerow([cpf.strip(),f.strip()])
                            break
                        else:
                            writer.writerow([cpf.strip(),'none'])
                            print("sem processo de teto")
            except:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/dl/dt/span')))
                if 'Sua pesquisa' in driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/dl/dt/span').text:
                    writer.writerow([cpf.strip(),'none'])
                    print("sem processo de teto")
                else:
                    raise Exception('')
            driver.close()
        except:
            writer.writerow([cpf.strip(),'erro'])
            print('erro encontrado, pulando cpf: '+cpf)
            pass
        n+=1

def main():
    o = open('output.txt', 'w+')
    writer=csv.writer(o)
    f = open("cpfs.txt", "r")
    reader=csv.reader(f, delimiter=',', quotechar='"')
    cpfs = f.readlines()
    t=[]
    T(10, t, writer, reader)
    for i in t:
        i.join()
    o.close()
    f.close()

if __name__ == '__main__':
    main()
